#!/usr/bin/python
# -*- coding: utf-8 -*-
"""module for media. It is a base for anime and manga module."""
from decimal import InvalidOperation
import abc
import decimal
import re

import bs4

try:
    from .anime import MalformedAnimePageError
    from .base import Base, MalformedPageError, InvalidBaseError, loadable
    from . import utilities
except ImportError:
    from . import utilities
    # from .anime import MalformedAnimePageError
    from .base import Base, MalformedPageError, InvalidBaseError, loadable


class MalformedMediaPageError(MalformedPageError):
    """Indicate that a media-related page on MAL has broken markup in some way."""

    pass


class InvalidMediaError(InvalidBaseError):
    """Indicate that the media requested does not exist on MAL."""

    pass


class Media(Base, metaclass=abc.ABCMeta):
    """Abstract base class for all media resources on MAL.

    To subclass, create a class that inherits from Media,
    implementing status_terms and consuming_verb at the bare minimum.
    """

    @abc.abstractproperty
    def _status_terms(self):
        """Get Status term of the media.

        :rtype: dict
        A status dict with::

          keys -- int statuses
          values -- string statuses e.g. "Airing"
        """
        pass

    @abc.abstractproperty
    def _consuming_verb(self):
        """Get media consuming verb.

        :rtype: str
        :return: the verb used to consume this media, e.g. "read"
        """
        pass

    @classmethod
    def newest(cls, session):
        """Fetche the latest media added to MAL.

        :type session: :class:`myanimelist.session.Session`
        :param session: A valid MAL session

        :rtype: :class:`.Media`
        :return: the newest media on MAL

        :raises: :class:`.MalformedMediaPageError`

        """
        media_type = cls.__name__.lower()
        p = session.session.get('http://myanimelist.net/' +
                                media_type + '.php?o=9&c[]=a&c[]=d&cv=2&w=1').text
        soup = utilities.get_clean_dom(p)
        latest_entry = soup.find("div", {"class": "hoverinfo"})
        if not latest_entry:
            raise MalformedMediaPageError(0, p, "No media entries found on recently-added page")
        latest_id = int(latest_entry['rel'][1:])
        return getattr(session, media_type)(latest_id)

    def __init__(self, session, id):
        """Create an instance of Media.

        :type session: :class:`myanimelist.session.Session`
        :param session: A valid MAL session.

        :type id: int
        :param id: The media's ID.

        :raises: :class:`.InvalidMediaError`

        """
        super(Media, self).__init__(session)
        self.id = id
        if not isinstance(self.id, int) or int(self.id) < 1:
            raise InvalidMediaError(self.id)
        self._title = None
        self._picture = None
        self._alternative_titles = None
        self._type = None
        self._status = None
        self._genres = None
        self._score = None
        self._rank = None
        self._popularity = None
        self._members = None
        self._favorites = None
        self._popular_tags = None
        self._synopsis = None
        self._related = None
        self._characters = None
        self._score_stats = None
        self._status_stats = None

    def parse_genres(self, media_page):
        """Parse the DOM and returns media genres in the sidebar.

        :type media_page: :class:`bs4.BeautifulSoup`
        :param media_page: MAL media page's DOM

        :rtype: list
        :return: media genres.
        """
        info_panel = media_page.select('div#content table td')[0]
        genres_tag = info_panel.find(text='Genres:').parent.parent
        # utilities.extract_tags(genres_tag.find_all(u'span', {'class': 'dark_text'}))
        genres = []
        for genre_link in genres_tag.find_all('a'):
            # genre_link e.g: '/anime/genre/29/Space'
            link_parts = genre_link.get('href').split('/')
            genre_id = int(link_parts[-2])
            genre_text = link_parts[-1]
            genre = self.session.genre(genre_id).set({'name': genre_text})
            genres.append(genre)
        return genres

    def parse_rank(self, media_page):
        """Parse the DOM and returns media rank.

        :type media_page: :class:`bs4.BeautifulSoup`
        :param media_page: MAL media page's DOM

        :return: media rank.
        """
        info_panel_first = media_page.select('div#content table td')[0]
        try:
            rank_tag = info_panel_first.find(text='Ranked:').parent.parent
            utilities.extract_tags(rank_tag.find_all())
            return int(rank_tag.text.strip()[1:].replace(',', ''))
        except AttributeError:
            rank_tag = [x for x in media_page.find_all('div', {'class': 'spaceit'}) if 'Ranked:' in x.text]
            return int(rank_tag[0].text.split('#')[-1].strip())
        except ValueError:
            rank_tag_txt = rank_tag.text.strip()[1:].replace(',', '')
            rank_tag_txt = rank_tag_txt.split('#')[1].splitlines()[0]
            return int(rank_tag_txt)

    def parse_picture(self, media_page):
        """Parse the DOM and returns media picture.

        :type media_page: :class:`bs4.BeautifulSoup`
        :param media_page: MAL media page's DOM

        :rtype: unicode
        :return: media picture
        """
        info_panel_first = media_page.select('div#content table td')[0]
        picture_tag = info_panel_first.find('img')
        try:
            return picture_tag.get('src').decode('utf-8')
        except AttributeError:
            return picture_tag.get('src')

    def parse_popularity(self, media_page):
        """Parse the DOM and returns media popularity rank.

        :type media_page: :class:`bs4.BeautifulSoup`
        :param media_page: MAL media page's DOM

        :rtype: int
        :return: media popularity rank
        """
        info_panel_first = media_page.select('div#content table td')[0]
        try:
            popularity_tag = info_panel_first.find(text='Popularity:').parent.parent
            utilities.extract_tags(popularity_tag.find_all())
            return int(popularity_tag.text.strip()[1:].replace(',', ''))
        except AttributeError:
            rank_tag_cls = {'class': 'dark_text'}
            rank_tag = filter(lambda x: 'Popularity' in x.text,
                              media_page.find_all('span', rank_tag_cls))[0].parent
            return int(rank_tag.text.split('#')[-1].strip())
        except ValueError:
            pop_txt = popularity_tag.text.strip()[1:].replace(',', '')
            return pop_txt.split('#')[1]

    def parse_members(self, media_page):
        """Parse the DOM and returns media member rank.

        :type media_page: :class:`bs4.BeautifulSoup`
        :param media_page: MAL media page's DOM

        :rtype: int
        :return: media member rank
        """
        info_panel_first = media_page.select('div#content table td')[0]
        try:
            members_tag = info_panel_first.find(text='Members:').parent.parent
            utilities.extract_tags(members_tag.find_all())
            return int(members_tag.text.strip().replace(',', ''))
        except AttributeError:
            members_tag_cls = {'class': 'dark_text'}
            members_tag_list = media_page.find_all('span', members_tag_cls)
            members_tag = filter(lambda x: 'Members' in x.text, members_tag_list)[0].parent
            members_tag = members_tag.text.split(':')[-1].strip().replace(',', '')
            return int(members_tag)
        except ValueError:
            members_txt = members_tag.text.strip().replace(',', '')
            members_txt = members_txt.splitlines()[1]
            return int(members_txt)

    def parse_favorites(self, media_page):
        """Parse the DOM and returns media favorite rank.

        :type media_page: :class:`bs4.BeautifulSoup`
        :param media_page: MAL media page's DOM

        :rtype: int
        :return: media favorite rank
        """
        info_panel_first = media_page.select('div#content table td')[0]
        try:
            favorites_tag = info_panel_first.find(text='Favorites:').parent.parent
            utilities.extract_tags(favorites_tag.find_all())
            return int(favorites_tag.text.strip().replace(',', ''))
        except AttributeError:
            favorites_tag_list = media_page.find_all('span', {'class': 'dark_text'})
            favorites_tag = filter(lambda x: 'Favorites' in x.text,
                                   favorites_tag_list)[0].parent
            favorites_tag = favorites_tag.text.split(':')[-1].strip().replace(',', '')
            return int(favorites_tag)
        except ValueError:
            favorites_txt = favorites_tag.text.strip().replace(',', '')
            return int(favorites_txt.splitlines()[1].strip())

    def parse_sidebar(self, media_page, media_page_original=None):
        """Parse the DOM and returns media attributes in the sidebar.

        :type media_page: :class:`bs4.BeautifulSoup`
        :param media_page: MAL media page's DOM

        :rtype: dict
        :return: media attributes.

        :raises: InvalidMediaError, MalformedMediaPageError

        """
        media_info = {}

        # if MAL says the series doesn't exist, raise an InvalidMediaError.
        error_tag = media_page.find('div', {'class': 'badresult'})
        if error_tag:
            raise InvalidMediaError(self.id)

        try:
            title_tag = media_page.find('div', {'id': 'contentWrapper'}).find('h1')
            if not title_tag.find('div'):
                try:
                    title_tag = media_page_original.select('div#contentWrapper h1.h1 span')[0]
                except IndexError:
                    # otherwise, raise a MalformedMediaPageError.
                    raise MalformedMediaPageError(self.id, None, message="Could not find title div")
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            utilities.extract_tags(title_tag.find_all())
            media_info['title'] = title_tag.text.strip()
            if media_info['title'] == '':
                media_info['title'] = media_page_original.find('span', {'itemprop': 'name'}).text
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        info_panel_first = media_page_original.select('div#content table td')[0]
        try:
            media_info['picture'] = self.parse_picture(media_page_original)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            # assemble alternative titles for this series.
            media_info['alternative_titles'] = {}
            alt_titles_header = info_panel_first.find('h2', text='Alternative Titles')
            if alt_titles_header:
                next_tag = alt_titles_header.find_next_sibling('div', {'class': 'spaceit_pad'})
                while True:
                    if next_tag is None or not next_tag.find('span', {'class': 'dark_text'}):
                        # not a language node, break.
                        break
                    # get language and remove the node.
                    language = next_tag.find('span').text[:-1]
                    utilities.extract_tags(next_tag.find_all('span', {'class': 'dark_text'}))
                    names = next_tag.text.strip().split(', ')
                    media_info['alternative_titles'][language] = names
                    next_tag = next_tag.find_next_sibling('div', {'class': 'spaceit_pad'})
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            try:
                type_tag = info_panel_first.find(text='Type:').parent.parent
                utilities.extract_tags(type_tag.find_all('span', {'class': 'dark_text'}))
                media_info['type'] = type_tag.text.strip()
            except AttributeError:
                type_tag = [x for x in info_panel_first.find_all('div') if 'Type:' in x.text][0]
                media_info['type'] = type_tag.text.split(':')[-1].strip()
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            status_tag = [x for x in media_page.find_all('span')if 'Status:' in x.text][0].parent
            media_info['status'] = status_tag.text.split(':')[1].strip()
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            media_info['genres'] = self.parse_genres(media_page_original)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            # grab statistics for this media.
            score_tag = media_page.find('span', {'itemprop': 'aggregateRating'})
            # there is difference between anime and manga page
            # in manga page score_tag is in span-tag and anime in div-page
            # test score tag by try to find span-tag
            try:
                score_tag.find('span')
            except AttributeError:
                score_tag = score_tag = media_page.find('div', {'itemprop': 'aggregateRating'})

            # get score and number of users.
            num_users_text = score_tag.find('span', {'itemprop': 'ratingCount'})
            num_users_text = num_users_text.text.replace(',', '')
            num_users = int(num_users_text)
            # utilities.extract_tags(score_tag.find_all())
            score_point = score_tag.find('span', {'itemprop': 'ratingValue'}).text
            try:
                media_info['score'] = (decimal.Decimal(score_point), num_users)
            except (InvalidOperation, AttributeError):
                score_tag = media_page_original.find('span', {'itemprop': 'ratingValue'})
                media_info['score'] = (decimal.Decimal(score_tag.text), num_users)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            media_info['rank'] = self.parse_rank(media_page_original)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            media_info['popularity'] = self.parse_popularity(media_page_original)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            media_info['members'] = self.parse_members(media_page_original)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            media_info['favorites'] = self.parse_favorites(media_page_original)

        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            # get popular tags.
            tags_header = media_page.find('h2', text='Popular Tags')
            try:
                tags_tag = tags_header.find_next_sibling('span')
                media_info['popular_tags'] = {}
                for tag_link in tags_tag.find_all('a'):
                    tag = self.session.tag(tag_link.text)
                    num_people = int(re.match(r'(?P<people>[0-9]+) people',
                                              tag_link.get('title')).group('people'))
                    media_info['popular_tags'][tag] = num_people
            except AttributeError:
                tags_tag = media_page_original.find('span', text='Genres:').parent
                media_info['popular_tags'] = {}
                for tag_link in tags_tag.find_all('a'):
                    tag = self.session.tag(tag_link.text.lower())
                    try:
                        num_people = int(re.match(r'(?P<people>[0-9]+) people',
                                                  tag_link.get('title')).group('people'))
                        media_info['popular_tags'][tag] = num_people
                    except (TypeError, AttributeError):
                        tag_num = tag_link.get('href').split('=')[-1]
                        media_info['popular_tags'][tag] = tag_num

        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return media_info

    def parse_related_media(self, media_page):
        """Parse the DOM and returns related media.

        :type media_page: :class:`bs4.BeautifulSoup`
        :param media_page: MAL media page's DOM

        :rtype: dict
        :return: related media attributes.

        """
        result_dict = {}
        # find table with related media
        table = media_page.find('table', {'class': 'anime_detail_related_anime'})
        # return None if table is not found
        if table is None:
            return None
        # if table is not None process the table
        for row in table.find_all('tr'):
            # TODO check if one category contain more than one media
            # find all cell in a row
            cells = row.find_all('td')
            # first cell containt category of related media like 'Adaptation' or 'Sequel'
            related_category = str(cells[0].text.split(':')[0])
            # second cell contain the media and it can contain multiple media
            # ie:<a href="/manga/9115/Ookami_to_Koushinryou">Ookami to Koushinryou</a>
            # temporarily containt the in list
            related_category_media_list = []
            for related_media_tag in cells[1].find_all('a'):
                # parsing the tag
                href_parts = related_media_tag.get('href').split('/')
                obj_id = int(href_parts[2])
                title = related_media_tag.text
                # create new object
                new_obj = getattr(self.session, href_parts[1])(obj_id).set({'title': title})
                related_category_media_list.append(new_obj)
            # return found all related media in a dict
            result_dict[related_category] = related_category_media_list
        # return None if nothing found instead empty dict
        if result_dict == {}:
            return None
        else:
            return result_dict

    def parse_synopsis(self, media_page):
        """Parse the DOM and returns media synopsis.

        :type media_page: :class:`bs4.BeautifulSoup`
        :param media_page: MAL media page's DOM

        :rtype: string
        :return: media synopsis.

        """
        synopsis_elt = [x for x in media_page.find_all('h2')
                        if "Synopsis" in x.text][0].parent
        # filter the text between 2 h2-tag
        temp_synopsis_elt = []
        for x in synopsis_elt.contents[1:]:
            if type(x) == bs4.element.Tag:
                if x.name == 'h2':
                    break
                temp_synopsis_elt.append(x.text)
            else:
                temp_synopsis_elt.append(x)
        synopsis_elt = ''.join(temp_synopsis_elt)
        try:
            utilities.extract_tags(synopsis_elt.find_all('h2'))
            result = synopsis_elt.text.strip()
        except AttributeError:
            # the current synopsis_elt may not contain any h2-tag
            result = synopsis_elt
        if result == '':
            # result tag
            rs_tag = [xx for xx in media_page.select('span')
                      if xx.get('itemprop') == 'description'][0]
            result = rs_tag.text
        return result

    def parse(self, media_page, media_page_original=None):
        """Parse the DOM and returns media attributes in the main-content area.

        :type media_page: :class:`bs4.BeautifulSoup`
        :param media_page: MAL media page's DOM

        :type media_page: :class:`bs4.BeautifulSoup`
        :param media_page: MAL media page's DOM unclean

        :rtype: dict
        :return: media attributes.

        """
        media_info = self.parse_sidebar(media_page, media_page_original)

        try:
            media_info['synopsis'] = self.parse_synopsis(media_page)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            related_title = media_page.find('h2', text='Related ' + self.__class__.__name__)
            if related_title:
                related_elt = related_title.parent
                utilities.extract_tags(related_elt.find_all('h2'))
                related = {}
                for link in related_elt.find_all('a'):
                    href = link.get('href').replace('http://myanimelist.net', '')
                    if not re.match(r'/(anime|manga)', href):
                        break
                    curr_elt = link.previous_sibling
                    if curr_elt is None:
                        # we've reached the end of the list.
                        break
                    related_type = None
                    while True:
                        if not curr_elt:
                            err_msg = "Prematurely reached end of related anime listing"
                            raise MalformedAnimePageError(self.id, related_elt,
                                                          message=err_msg)
                        if isinstance(curr_elt, bs4.NavigableString):
                            type_match = re.match('(?P<type>[a-zA-Z\ \-]+):', curr_elt)
                            if type_match:
                                related_type = type_match.group('type')
                                break
                        curr_elt = curr_elt.previous_sibling
                    title = link.text
                    # parse link: may be manga or anime.
                    href_parts = href.split('/')
                    # sometimes links on MAL are broken, of the form /anime//
                    if href_parts[2] == '':
                        continue
                    # of the form: /(anime|manga)/1/Cowboy_Bebop
                    obj_id = int(href_parts[2])
                    new_obj = getattr(self.session, href_parts[1])(obj_id).set({'title': title})
                    if related_type not in related:
                        related[related_type] = [new_obj]
                    else:
                        related[related_type].append(new_obj)
                media_info['related'] = related
            else:
                media_info['related'] = None

            # check once again using a single function if the first method found none
            if media_info['related'] is None:
                media_info['related'] = self.parse_related_media(media_page_original)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return media_info

    def parse_stats(self, media_page):
        """Parse the DOM and returns media statistics attributes.

        :type media_page: :class:`bs4.BeautifulSoup`
        :param media_page: MAL media stats page's DOM

        :rtype: dict
        :return: media stats attributes.

        """
        media_info = self.parse_sidebar(media_page)
        verb_progressive = self.consuming_verb + 'ing'
        status_stats = {
            verb_progressive: 0,
            'completed': 0,
            'on_hold': 0,
            'dropped': 0,
            'plan_to_' + self.consuming_verb: 0
        }
        try:
            consuming_elt = media_page.find('span', {'class': 'dark_text'},
                                            text=verb_progressive.capitalize())
            if consuming_elt:
                verb_progressive_num = consuming_elt.nextSibling.strip().replace(',', '')
                status_stats[verb_progressive] = int(verb_progressive_num)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            completed_elt = media_page.find('span', {'class': 'dark_text'}, text="Completed:")
            if completed_elt:
                completed_num = completed_elt.nextSibling.strip().replace(',', '')
                status_stats['completed'] = int(completed_num)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            on_hold_elt = media_page.find('span', {'class': 'dark_text'}, text="On-Hold:")
            if on_hold_elt:
                status_stats['on_hold'] = int(on_hold_elt.nextSibling.strip().replace(',', ''))
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            dropped_elt = media_page.find('span', {'class': 'dark_text'}, text="Dropped:")
            if dropped_elt:
                status_stats['dropped'] = int(dropped_elt.nextSibling.strip().replace(',', ''))
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            planning_elt = media_page.find('span', {'class': 'dark_text'},
                                           text="Plan to " + self.consuming_verb.capitalize() + ":")
            if planning_elt:
                status_stats['plan_to_' + self.consuming_verb] = int(
                    planning_elt.nextSibling.strip().replace(',', ''))
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        media_info['status_stats'] = status_stats

        score_stats = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0
        }
        try:
            score_stats_header = media_page.find('h2', text='Score Stats')
            if score_stats_header:
                score_stats_table = score_stats_header.find_next_sibling('table')
                if score_stats_table:
                    score_stats = {}
                    score_rows = score_stats_table.find_all('tr')
                    for i in range(len(score_rows)):
                        score_value = int(score_rows[i].find('td').text)
                        score_value_num = score_rows[i].find('small').text.replace('(u', '')
                        score_value_num = score_value_num.replace(' votes)', '')
                        score_stats[score_value] = int(score_value_num)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        media_info['score_stats'] = score_stats

        return media_info

    def parse_characters(self, character_page, character_page_original=None):
        """Parse the DOM and returns media character attributes in the sidebar.

        :type character_page: :class:`bs4.BeautifulSoup`
        :param character_page: MAL character page's DOM

        :rtype: dict
        :return: character attributes.

        """
        media_info = self.parse_sidebar(character_page, character_page_original)

        try:
            character_title = [x for x in character_page.find_all('h2') if 'Characters' in x.text]
            media_info['characters'] = {}
            if character_title:
                character_title = character_title[0]
                curr_elt = character_title.find_next_sibling('table')
                while curr_elt:
                    curr_row = curr_elt.find('tr')
                    # character in second col.
                    character_col = curr_row.find_all('td', recursive=False)[1]
                    character_link = character_col.find('a')
                    character_name = ' '.join(reversed(character_link.text.split(', ')))
                    link_parts = character_link.get('href').split('/')
                    # of the form /character/7373/Holo
                    char_id = int(link_parts[2])
                    character = self.session.character(char_id).set({'name': character_name})
                    role = character_col.find('small').text
                    media_info['characters'][character] = {'role': role}
                    curr_elt = curr_elt.find_next_sibling('table')
            if media_info['characters'] == {}:
                character_title = [x for x in character_page_original.find_all('h2') if 'Characters' in x.text]
                tables = character_title[0].findNextSiblings('table')
                for table in tables:
                    # one table only contain one row which contain 2 cell, which are photo , text
                    # get second cell
                    character_col = table.find_all('td')[1]
                    # find link in that cell
                    character_link = character_col.find('a')
                    # find char name and reverse it
                    character_name = ' '.join(reversed(character_link.text.split(', ')))
                    # get role which written in small-tag
                    role = character_col.find('small').text
                    # get link and split with splash
                    # of the form /character/7373/Holo
                    link_parts = character_link.get('href').split('/')
                    # create object
                    char_id = int(link_parts[2])
                    character = self.session.character(char_id).set({'name': character_name})
                    media_info['characters'][character] = {'role': role}
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return media_info

    def load(self):
        """Fetche the MAL media page and sets the current media's attributes.

        :rtype: :class:`.Media`
        :return: current media object.

        """
        media_page = self.session.session.get(
            'http://myanimelist.net/' + self.__class__.__name__.lower() + '/' + str(self.id)).text
        media_page_original = bs4.BeautifulSoup(media_page, 'lxml')
        self.set(self.parse(utilities.get_clean_dom(media_page), media_page_original))
        return self

    def load_stats(self):
        """Fetche the MAL media statistics page and sets the current media's statistics attributes.

        :rtype: :class:`.Media`
        :return: current media object.

        """
        stats_page = self.session.session.get('http://myanimelist.net/' +
                                              self.__class__.__name__.lower() + '/' +
                                              str(self.id) + '/' +
                                              utilities.urlencode(self.title) + '/stats').text
        self.set(self.parse_stats(utilities.get_clean_dom(stats_page)))
        return self

    def load_characters(self):
        """Fetche the MAL media characters page and sets the current media's character attributes.

        :rtype: :class:`.Media`
        :return: current media object.

        """
        character_page_url = ('http://myanimelist.net/' + self.__class__.__name__.lower() +
                              '/' + str(self.id) + '/' + utilities.urlencode(self.title) +
                              '/characters')
        characters_page = self.session.session.get(character_page_url).text
        characters_page_original = bs4.BeautifulSoup(characters_page, 'lxml')
        self.set(self.parse_characters(utilities.get_clean_dom(characters_page),
                                       characters_page_original))
        return self

    @property
    @loadable('load')
    def title(self):
        """Get Media's title."""
        return self._title

    @property
    @loadable('load')
    def picture(self):
        """URL of media's primary pictures."""
        return self._picture

    @property
    @loadable('load')
    def alternative_titles(self):
        """Alternative titles dict.

        with types of titles, e.g. 'Japanese', 'English', or 'Synonyms' as keys,
        and lists of said alternative titles as values.
        """
        return self._alternative_titles

    @property
    @loadable('load')
    def type(self):
        """Type of this media, e.g. 'TV' or 'Manga' or 'Movie'."""
        return self._type

    @property
    @loadable('load')
    def status(self):
        """Publication status, e.g. 'Finished Airing'."""
        return self._status

    @property
    @loadable('load')
    def genres(self):
        """A list of :class:`myanimelist.genre.Genre` objects associated with this media."""
        return self._genres

    @property
    @loadable('load')
    def score(self):
        """get media score.

        A tuple(2) containing an instance of decimal.Decimal.
        it is storing the aggregate score, weighted or non-weighted,
        and an int storing the number of ratings

        """
        return self._score

    @property
    @loadable('load')
    def rank(self):
        """Score rank."""
        return self._rank

    @property
    @loadable('load')
    def popularity(self):
        """Popularity rank."""
        return self._popularity

    @property
    @loadable('load')
    def members(self):
        """Number of members."""
        return self._members

    @property
    @loadable('load')
    def favorites(self):
        """Number of users who favourited this media."""
        return self._favorites

    @property
    @loadable('load')
    def popular_tags(self):
        """get Media tags.

        Tags dict with :class:`myanimelist.tag.Tag` objects as keys,
        and the number of tags as values.
        """
        return self._popular_tags

    @property
    @loadable('load')
    def synopsis(self):
        """Media synopsis."""
        return self._synopsis

    @property
    @loadable('load')
    def related(self):
        """Related media dict.

        It have strings of relation types, e.g. 'Sequel' as keys,
        and lists containing instances of :class:`.Media` subclasses as values.
        """
        return self._related

    @property
    @loadable('load_characters')
    def characters(self):
        """Character dict.

        It have :class:`myanimelist.character.Character` objects as keys,
        and a dict with attributes of this role, e.g. 'role': 'Main' as values.
        """
        return self._characters

    @property
    @loadable('load_stats')
    def status_stats(self):
        """Get status statistics dict.

        It have strings of statuses, e.g. 'on_hold' as keys, and an int number of users as values.
        """
        return self._status_stats

    @property
    @loadable('load_stats')
    def score_stats(self):
        """Score statistics dict.

        It have int scores from 1-10 as keys, and an int number of users as values.
        """
        return self._score_stats
