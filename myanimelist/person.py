#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Parser for person page."""
import utilities
from base import Base, MalformedPageError, InvalidBaseError, loadable


class MalformedPersonPageError(MalformedPageError):
    """Indicates that an person-related page on MAL has irreparably broken markup in some way."""

    pass


class InvalidPersonError(InvalidBaseError):
    """Indicates that the requested person does not exist on MAL."""

    pass


class Person(Base):
    """Class for person."""

    def __init__(self, session, person_id):
        """init person object given the session and person id."""
        super(Person, self).__init__(session)
        self.id = person_id
        if not isinstance(self.id, int) or int(self.id) < 1:
            raise InvalidPersonError(self.id)
        self._name = None

        self._voice_acting_roles = None
        self._anime_staff_positions = None
        self._published_manga = None

    def load(self):
        """Fetche the MAL person page and sets the current person's attributes.

        :rtype: :class:`.Person`
        :return: Current person object.

        """
        person = self.session.session.get(u'http://myanimelist.net/people/' + str(self.id)).text
        self.set(self.parse(utilities.get_clean_dom(person)))
        return self

    def load_pictures(self):
        """Fetche the MAL person pictures page and sets the current character's pictures attributes.

        :rtype: :class:`.Person`
        :return: Current person object.

        """
        person = self.session.session.get(
            u'http://myanimelist.net/person/' + str(self.id) + u'/' + utilities.urlencode(
                self.name) + u'/pictures').text
        self.set(self.parse_pictures(utilities.get_clean_dom(person)))
        return self

    def parse(self, person_page):
        """Parse the DOM and returns person attributes in the main-content area.

        :type character_page: :class:`bs4.BeautifulSoup`
        :param character_page: MAL person page's DOM

        :rtype: dict
        :return: Person attributes.

        """
        def merge_two_dicts(x, y):
            """Given two dicts, merge them into a new dict as a shallow copy."""
            z = x.copy()
            z.update(y)
            return z
        person_info = self.parse_sidebar(person_page)
        person_info = merge_two_dicts(person_info, self.parse_name(person_page))
        person_info = merge_two_dicts(person_info, self.parse_role(person_page))
        person_info = merge_two_dicts(person_info, self.parse_position(person_page))
        return person_info

    def _fix_name(self, name):
                """Reverse the family name and given name in a name.

                when a given name with comma inside it will reverse the order of the name.
                ie 'abad, kajfk' to 'kajfk abad'

                :type name: name
                :param name: a person name

                :rtype: dict
                :return: fixed name.
                """
                if ',' not in name:
                    return name
                else:
                    name_parts = name.split(',')
                    return '{} {}'.format(name_parts[1].strip(), name_parts[0].strip())

    def parse_name(self, person_page):
        """find name in person page."""
        try:
            person_info = {}
            temp_name = person_page.select('div#contentWrapper h1.h1')[0].text
            person_info[u'name'] = self._fix_name(temp_name)
            if person_info[u'name'] == 'Invalid':
                raise InvalidPersonError(self.id)
        except:
            if not self.session.suppress_parse_exceptions:
                raise
        return person_info

    def parse_role(self, person_page):        # parsing person role in anime
        """find role in person page."""
        try:
            person_info = {}
            table_sibling = [tag for tag in person_page.select('div.normal_header')
                             if 'Voice Acting Roles' in tag.text][0]
            va_roles_tags = table_sibling.parent.find('table').find_all('tr')
            va_roles = {}
            for va_tag in va_roles_tags:
                a_tags = va_tag.find_all('a')

                # find anime
                anime_tag = [xx for xx in a_tags if '/anime/' in xx.get('href')][0]
                # ie '/anime/6547/Angel_Beats'
                anime_id = anime_tag.get('href').split('/')[2]
                anime_title = anime_tag.text
                anime_obj = self.session.anime(int(anime_id)).set({'title': anime_title})

                # from the anime find character ie 'otonashi yuzuru'
                # this will return IndexError if the person don't have voice acting role
                char_tag = [xx for xx in a_tags if '/character/' in xx.get('href')][0]
                # ie '/character/24502/Yuzuru_Otonashi'
                character_id = int(char_tag.get('href').split('/')[2])
                character_name = self._fix_name(char_tag.text)
                character_obj = self.session.character(character_id).set({'name': character_name})

                # find the role for the said character ie 'main'
                role_tag = va_tag.find_all('td')[2].find('div').text.strip()

                # create a dict which will be merged into va_roles dict
                va_roles[anime_obj] = {character_obj: role_tag}

            # add as person attribute
            person_info[u'voice_acting_roles'] = va_roles

        except IndexError:
            # this person don't have any voice acting roles
            person_info[u'voice_acting_roles'] = None

        except:
            if not self.session.suppress_parse_exceptions:
                raise
        return person_info

    def parse_position(self, person_page):
        """find person position in anime production."""
        try:
            person_info = {}
            table_siblings = [tag for tag in person_page.select('div.normal_header')
                              if 'Anime Staff Positions' in tag.text]
            table_sibling = table_siblings[0]
            position_tables = table_sibling.parent.find_all('table')
            # check if position table only have  1table
            if len(position_tables) < 2:
                position_tags = []
            else:
                position_tags = position_tables[1].find_all('tr')
            positions = {}
            for position_tag in position_tags:
                a_tags = position_tag.find_all('a')

                # find anime
                anime_tags = [xx for xx in a_tags if '/anime/' in xx.get('href')]
                if len(anime_tags) != 0:
                    anime_tag = anime_tags[0]
                else:
                    continue
                # ie '/anime/6547/Angel_Beats'
                anime_id = anime_tag.get('href').split('/')[2]
                anime_title = anime_tag.text
                anime_obj = self.session.anime(int(anime_id)).set({'title': anime_title})

                # find the for the said character ie 'main'
                role_tag = position_tag.find_all('td')[1].find('div').find('small').text.strip()

                try:
                    # append dict to position
                    positions[anime_obj].append(role_tag)
                except KeyError:
                    positions[anime_obj] = [role_tag]

            # add as person attribute only if dict have been changed
            if positions == {}:
                person_info[u'anime_staff_positions'] = None
            else:
                person_info[u'anime_staff_positions'] = positions

        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return person_info

    def parse_sidebar(self, person_page):
        """Parse the DOM and returns person attributes in the sidebar.

        :type character_page: :class:`bs4.BeautifulSoup`
        :param character_page: MAL person page's DOM

        :rtype: dict
        :return: person attributes

        :raises: :class:`.InvalidCharacterError`, :class:`.MalformedCharacterPageError`
        """
        person_info = {}
        # TODO

        return person_info

    def parse_pictures(self, picture_page):
        """Parse the DOM and returns person pictures attributes.

        :type picture_page: :class:`bs4.BeautifulSoup`
        :param picture_page: MAL person pictures page's DOM

        :rtype: dict
        :return: person pictures attributes.

        """
        # TODO
        pass

    @property
    @loadable(u'load')
    def name(self):
        """name of the person."""
        return self._name

    @property
    @loadable(u'load')
    def voice_acting_roles(self):
        """voice acting role done by this person."""
        return self._voice_acting_roles

    @property
    @loadable(u'load')
    def anime_staff_positions(self):
        """Position of this person on anime production."""
        return self._anime_staff_positions
