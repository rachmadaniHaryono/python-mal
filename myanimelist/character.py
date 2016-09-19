#!/usr/bin/python
# -*- coding: utf-8 -*-
"""module for character."""

# import bs4
import re

try:
    import utilities
    from base import Base, MalformedPageError, InvalidBaseError, loadable
except ImportError:
    from . import utilities
    from .base import Base, MalformedPageError, InvalidBaseError, loadable


class MalformedCharacterPageError(MalformedPageError):
    """Indicates that a character-related page on MAL has irreparably broken markup in some way."""

    pass


class InvalidCharacterError(InvalidBaseError):
    """Indicates that the character requested does not exist on MAL."""

    pass


class Character(Base):
    """Primary interface to character resources on MAL."""

    def __init__(self, session, character_id):
        """Creates a new instance of Character.

        :type session: :class:`myanimelist.session.Session`
        :param session: A valid MAL session
        :type character_id: int
        :param character_id: The desired character's ID on MAL

        :raises: :class:`.InvalidCharacterError`

        """
        super(Character, self).__init__(session)
        self.id = character_id
        if not isinstance(self.id, int) or int(self.id) < 1:
            raise InvalidCharacterError(self.id)
        self._name = None
        self._full_name = None
        self._name_jpn = None
        self._description = None
        self._voice_actors = None
        self._animeography = None
        self._mangaography = None
        self._num_favorites = None
        self._favorites = None
        self._picture = None
        self._pictures = None
        self._clubs = None

    def parse_char_picture(self, character_page):
        """Parse the DOM and returns character picture.

        :type character_page: :class:`bs4.BeautifulSoup`
        :param character_page: MAL character page's DOM

        :type character_page: :class:`bs4.BeautifulSoup`
        :param character_page: MAL character page's DOM uncleaned

        :rtype: str
        :return: Character picture
        """
        cls_attr = {'id': 'content'}
        info_panel_first = character_page.find('div', cls_attr).find('table').find('td')
        picture_tag = info_panel_first.find('img')
        try:
            return picture_tag.get('src').decode('utf-8')
        except AttributeError:
            return picture_tag.get('src')

    def parse_sidebar(self, character_page, character_page_original=None):
        """Parse the DOM and returns character attributes in the sidebar.

        :type character_page: :class:`bs4.BeautifulSoup`
        :param character_page: MAL character page's DOM

        :type character_page: :class:`bs4.BeautifulSoup`
        :param character_page: MAL character page's DOM uncleaned

        :rtype: dict
        :return: Character attributes

        :raises: :class:`.InvalidCharacterError`, :class:`.MalformedCharacterPageError`
        """
        character_info = {}

        error_tag = character_page.find('div', {'class': 'badresult'})
        if error_tag:
            # MAL says the character does not exist.
            raise InvalidCharacterError(self.id)

        try:
            full_name_tag = character_page.find('div', {'id': 'contentWrapper'}).find('h1')
            if not full_name_tag:
                # Page is malformed.
                raise MalformedCharacterPageError(self.id, html, message="Could not find title div")
            character_info['full_name'] = full_name_tag.text.strip()
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        info_panel_first = character_page.find('div', {'id': 'content'}).find('table').find('td')

        try:
            picture_tag = info_panel_first.find(u'img')
            try:
                character_info[u'picture'] = picture_tag.get(u'src').decode('utf-8')
            except AttributeError:
                character_info[u'picture'] = picture_tag.get(u'src')

        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            # assemble animeography for this character.
            character_info['animeography'] = {}
            animeography_header = info_panel_first.find('div', text='Animeography')
            if animeography_header:
                animeography_table = animeography_header.find_next_sibling('table')
                for row in animeography_table.find_all('tr'):
                    # second column has anime info.
                    info_col = row.find_all('td')[1]
                    anime_link = info_col.find('a')
                    link_parts = anime_link.get('href').split('/')
                    # of the form: /anime/1/Cowboy_Bebop
                    anime = self.session.anime(int(link_parts[2])).set({'title': anime_link.text})
                    role = info_col.find('small').text
                    character_info['animeography'][anime] = role
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            # assemble mangaography for this character.
            character_info['mangaography'] = {}
            mangaography_header = info_panel_first.find('div', text='Mangaography')
            if mangaography_header:
                mangaography_table = mangaography_header.find_next_sibling('table')
                for row in mangaography_table.find_all('tr'):
                    # second column has manga info.
                    info_col = row.find_all('td')[1]
                    manga_link = info_col.find('a')
                    link_parts = manga_link.get('href').split('/')
                    # of the form: /manga/1/Cowboy_Bebop
                    manga = self.session.manga(int(link_parts[2])).set({'title': manga_link.text})
                    role = info_col.find('small').text
                    character_info['mangaography'][manga] = role
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            num_favorites_node = info_panel_first.find(text=re.compile('Member Favorites: '))
            character_info['num_favorites'] = int(num_favorites_node.strip().split(': ')[1])
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return character_info

    def parse(self, character_page):
        """Parses the DOM and returns character attributes in the main-content area.

        :type character_page: :class:`bs4.BeautifulSoup`
        :param character_page: MAL character page's DOM

        :rtype: dict
        :return: Character attributes.

        """
        character_info = self.parse_sidebar(character_page)

        second_col = \
            character_page.find('div', {'id': 'content'}).find('table').find('tr').find_all('td', recursive=False)[
                1]
        name_elt = second_col.find('div', {'class': 'normal_header'})

        try:
            name_jpn_node = name_elt.find('small')
            if name_jpn_node:
                character_info['name_jpn'] = name_jpn_node.text[1:-1]
            else:
                character_info['name_jpn'] = None
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            name_elt.find('span').extract()
            character_info['name'] = name_elt.text.rstrip()
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            description_elts = []
            curr_elt = name_elt.nextSibling
            while True:
                if curr_elt.name not in [None, 'br']:
                    break
                description_elts.append(str(curr_elt))
                curr_elt = curr_elt.nextSibling
            character_info['description'] = ''.join(description_elts)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            character_info['voice_actors'] = {}
            voice_actors_header = second_col.find('div', text='Voice Actors')
            if voice_actors_header:
                voice_actors_table = voice_actors_header.find_next_sibling('table')
                try:
                    # will raise attribute error when no va found
                    for row in voice_actors_table.find_all('tr'):
                        # second column has va info.
                        info_col = row.find_all('td')[1]
                        voice_actor_link = info_col.find('a')
                        name = ' '.join(reversed(voice_actor_link.text.split(', ')))
                        link_parts = voice_actor_link.get('href').split('/')
                        # of the form: /people/82/Romi_Park
                        person = self.session.person(int(link_parts[2])).set({'name': name})
                        language = info_col.find('small').text
                        character_info['voice_actors'][person] = language
                except AttributeError:
                        character_info['voice_actors'] = None

        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return character_info

    def parse_favorites(self, favorites_page):
        """Parses the DOM and returns character favorites attributes.

        :type favorites_page: :class:`bs4.BeautifulSoup`
        :param favorites_page: MAL character favorites page's DOM

        :rtype: dict
        :return: Character favorites attributes.

        """
        character_info = self.parse_sidebar(favorites_page)
        second_col = \
            favorites_page.find('div', {'id': 'content'}).find('table').find('tr').find_all('td', recursive=False)[
                1]

        try:
            character_info['favorites'] = []
            favorite_links = second_col.find_all('a', recursive=False)
            for link in favorite_links:
                # of the form /profile/shaldengeki
                character_info['favorites'].append(self.session.user(username=link.text))
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return character_info

    def parse_pictures(self, picture_page):
        """Parse the DOM and returns character pictures attributes.

        :type picture_page: :class:`bs4.BeautifulSoup`
        :param picture_page: MAL character pictures page's DOM

        :rtype: dict
        :return: character pictures attributes.

        """
        character_info = self.parse_sidebar(picture_page)
        second_col = (picture_page.find(
            u'div', {'id': 'content'}
        ).find(u'table').find(u'tr').find_all(u'td', recursive=False)[1])

        try:
            picture_table = second_col.find('table', recursive=False)
            character_info['pictures'] = []
            if picture_table:
                c_pictures = list(map(
                    lambda img: img.get(u'src'),
                    picture_table.find_all(u'img')
                ))
                try:
                    character_info[u'pictures'] = [x.decode('utf-8') for x in c_pictures]
                except AttributeError:
                    character_info[u'pictures'] = c_pictures
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return character_info

    def parse_clubs(self, clubs_page):
        """Parses the DOM and returns character clubs attributes.

        :type clubs_page: :class:`bs4.BeautifulSoup`
        :param clubs_page: MAL character clubs page's DOM

        :rtype: dict
        :return: character clubs attributes.

        """
        character_info = self.parse_sidebar(clubs_page)
        second_col = \
            clubs_page.find('div', {'id': 'content'}).find('table').find('tr').find_all('td', recursive=False)[1]

        try:
            clubs_header = second_col.find('div', text='Related Clubs')
            character_info['clubs'] = []
            if clubs_header:
                curr_elt = clubs_header.nextSibling
                while curr_elt is not None:
                    if curr_elt.name == 'div':
                        link = curr_elt.find('a')
                        club_id = int(re.match(r'/clubs\.php\?cid=(?P<id>[0-9]+)', link.get('href')).group('id'))
                        num_members = int(
                            re.match(r'(?P<num>[0-9]+) members', curr_elt.find('small').text).group('num'))
                        character_info['clubs'].append(
                            self.session.club(club_id).set({'name': link.text, 'num_members': num_members}))
                    curr_elt = curr_elt.nextSibling
        except:
            if not self.session.suppress_parse_exceptions:
                raise
        
        # second method if the method return none in character_info[u'clubs']
        try:
            if len(character_info['clubs']) == 0:
                clubs = clubs_page.select('div.borderClass')
                for club_tag in clubs:
                    club_id = int(club_tag.find('a').get('href').split('=')[-1])
                    link = club_tag.find('a')
                    num_members = club_tag.find('small').text
                    character_info['clubs'].append(
                                                self.session.club(club_id).set({'name': link.text, 'num_members': num_members}))
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return character_info

    def load(self):
        """Fetches the MAL character page and sets the current character's attributes.

        :rtype: :class:`.Character`
        :return: Current character object.

        """
        character = self.session.session.get('http://myanimelist.net/character/' + str(self.id)).text
        self.set(self.parse(utilities.get_clean_dom(character)))
        return self

    def load_favorites(self):
        """Fetches the MAL character favorites page.
        After that it sets the current character's favorites attributes.

        .. deprecated:: 0.1.8
        """
        pass

    def load_pictures(self):
        """Fetches the MAL character pictures page and sets the current character's pictures attributes.

        :rtype: :class:`.Character`
        :return: Current character object.

        """
        character = self.session.session.get(
            'http://myanimelist.net/character/' + str(self.id) + '/' + utilities.urlencode(
                self.name) + '/pictures').text
        self.set(self.parse_pictures(utilities.get_clean_dom(character)))
        return self

    def load_clubs(self):
        """Fetches the MAL character clubs page and sets the current character's clubs attributes.

        :rtype: :class:`.Character`
        :return: Current character object.

        """
        character = self.session.session.get(
            'http://myanimelist.net/character/' + str(self.id) + '/' + utilities.urlencode(
                self.name) + '/clubs').text
        self.set(self.parse_clubs(utilities.get_clean_dom(character)))
        return self

    @property
    @loadable('load')
    def name(self):
        """Character name.
        """
        return self._name

    @property
    @loadable('load')
    def full_name(self):
        """Character's full name.
        """
        return self._full_name

    @property
    @loadable('load')
    def name_jpn(self):
        """Character's Japanese name.
        """
        return self._name_jpn

    @property
    @loadable('load')
    def description(self):
        """Character's description.
        """
        return self._description

    @property
    @loadable('load')
    def voice_actors(self):
        """Voice actor dict for this character, with :class:`myanimelist.person.Person` objects as keys and the language as values.
        """
        return self._voice_actors

    @property
    @loadable('load')
    def animeography(self):
        """Anime appearance dict for this character, with :class:`myanimelist.anime.Anime` objects as keys and the type of role as values, e.g. 'Main'
        """
        return self._animeography

    @property
    @loadable('load')
    def mangaography(self):
        """Manga appearance dict for this character, with :class:`myanimelist.manga.Manga` objects as keys and the type of role as values, e.g. 'Main'
        """
        return self._mangaography

    @property
    @loadable('load')
    def num_favorites(self):
        """Number of users who have favourited this character.
        """
        return self._num_favorites

    @property
    @loadable('load_favorites')
    def favorites(self):
        """List of users who have favourited this character.
        """
        return self._favorites

    @property
    @loadable('load')
    def picture(self):
        """URL of primary picture for this character.
        """
        return self._picture

    @property
    @loadable('load_pictures')
    def pictures(self):
        """List of picture URLs for this character.
        """
        return self._pictures

    @property
    @loadable('load_clubs')
    def clubs(self):
        """List of clubs relevant to this character.
        """
        return self._clubs
