#!/usr/bin/python
# -*- coding: utf-8 -*-
"""module for media."""
import abc
import decimal
import re
import warnings
from decimal import InvalidOperation

import bs4

try:
    import utilities
    from base import Base, MalformedPageError, InvalidBaseError, loadable
except ImportError:
    from . import utilities
    from .base import Base, MalformedPageError, InvalidBaseError, loadable

# from anime import MalformedAnimePageError

class MalformedMediaPageError(MalformedPageError):
    """Indicates that a media-related page on MAL has broken markup in some way.
    """
    pass


class InvalidMediaError(InvalidBaseError):
    """Indicates that the media requested does not exist on MAL.
    """
    pass


class Media(Base):
    """Abstract base class for all media resources on MAL.

    To subclass, create a class that inherits from Media, implementing status_terms and consuming_verb at the bare minimum.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def _status_terms(self):
        """
        :rtype: dict
        A status dict with::

          keys -- int statuses
          values -- string statuses e.g. "Airing"
        """
        pass

    @abc.abstractproperty
    def _consuming_verb(self):
        """
        :rtype: str
        :return: the verb used to consume this media, e.g. "read"
        """
        pass

    @classmethod
    def newest(cls, session):
        """Fetches the latest media added to MAL.

        :type session: :class:`myanimelist.session.Session`
        :param session: A valid MAL session

        :rtype: :class:`.Media`
        :return: the newest media on MAL

        :raises: :class:`.MalformedMediaPageError`

        """
        media_type = cls.__name__.lower()
        p = session.session.get(u'http://myanimelist.net/' + media_type + '.php?o=9&c[]=a&c[]=d&cv=2&w=1').text
        soup = utilities.get_clean_dom(p)
        latest_entry = soup.find(u"div", {u"class": u"hoverinfo"})
        if not latest_entry:
            raise MalformedMediaPageError(0, p, u"No media entries found on recently-added page")
        latest_id = int(latest_entry[u'rel'][1:])
        return getattr(session, media_type)(latest_id)

    def __init__(self, session, id):
        """Creates an instance of Media.

        :type session: :class:`myanimelist.session.Session`
        :param session: A valid MAL session.

        :type id: int
        :param id: The media's ID.

        :raises: :class:`.InvalidMediaError`

        """
        try:
            super(Media, self).__init__(session)
        except TypeError:
            pass
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

    def _get_alternative_titles(self, html_tag):
        """get alternative_titles from html_tag."""
        alt_titles_header = html_tag.find(u'h2', text=u'Alternative Titles')
        result = {}

        if alt_titles_header:
            next_tag = alt_titles_header.find_next_sibling(u'div', {'class': 'spaceit_pad'})
            while True:
                if next_tag is None or not next_tag.find(u'span', {'class': 'dark_text'}):
                    # not a language node, break.
                    break
                # language tag have following form
                # <div><span>English:</span> english alternative text</div>
                # when converted into text will have following form
                # '\nEnglish: Cowboy Bebop\n  '
                # so split by char ':' and strip whitespace for both vars
                # alt title may also splitted by ',',
                # '\nEnglish: alt_titl1, alt_title2\n  '
                # but it doesn't clear if there is another way to render that
                # so split alt title by ',' naively
                tag_texts = next_tag.text.split(':', 1)
                language = tag_texts[0].strip()
                alt_title = [x.strip() for x in tag_texts[1].strip().split(',')]

                # append to result
                if language not in result:
                    result[language] = alt_title
                else:
                    result[language].extend(alt_title)
                # get next tag.
                next_tag = next_tag.find_next_sibling(u'div', {'class': 'spaceit_pad'})

            # while ended and return result
            return result

        else:
            # send empty dict when no alternative titles found.
            return {}

    def parse_sidebar(self, media_page, media_page_original=None):
        """Parses the DOM and returns media attributes in the sidebar.

        :type media_page: :class:`bs4.BeautifulSoup`
        :param media_page: MAL media page's DOM

        :rtype: dict
        :return: media attributes.

        :raises: InvalidMediaError, MalformedMediaPageError

        """
        media_info = {}

        # if MAL says the series doesn't exist, raise an InvalidMediaError.
        error_tag = media_page.find(u'div', {'class': 'badresult'})
        if error_tag:
            raise InvalidMediaError(self.id)

        try:
            title_tag = media_page.find(u'div', {'id': 'contentWrapper'}).find(u'h1')
            if not title_tag.find(u'div'):
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
            media_info[u'title'] = title_tag.text.strip()
            if media_info[u'title'] == '':
                media_info[u'title'] = media_page_original.find('span',{'itemprop':'name'}).text 
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        # info_panel_first = media_page.find(u'div', {'id': 'content'}).find(u'table').find(u'td')
        info_panel_first =  media_page_original.select('div#content table td')[0]
        try:
            picture_tag = info_panel_first.find(u'img')
            media_info[u'picture'] = picture_tag.get('src')
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            # assemble alternative titles for this series.
            media_info[u'alternative_titles'] = self._get_alternative_titles(info_panel_first)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
                type_tag = info_panel_first.find(text=u'Type:').parent.parent
                media_info[u'type'] = type_tag.text.split(':')[1].strip()
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            status_tag = [x for x in media_page.find_all('span')if 'Status:' in x.text][0].parent
            media_info[u'status'] = status_tag.text.split(':')[1].strip()
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            genres_tag = info_panel_first.find(text=u'Genres:').parent.parent
            # utilities.extract_tags(genres_tag.find_all(u'span', {'class': 'dark_text'}))
            media_info[u'genres'] = []
            for genre_link in genres_tag.find_all('a'):
                link_parts = genre_link.get('href').split('=')
                # of the form /anime|manga.php?genre[]=1
                try:
                    genre_id = int(link_parts[-1])
                except:
                    # for current form
                    # '/anime/genre/2/Adventure'
                    genre_id = int(link_parts[-1].split('/genre/')[1].split('/')[0])

                genre = self.session.genre(genre_id).set({'name': genre_link.text})
                media_info[u'genres'].append(genre)
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
            num_users = int(score_tag.find('span', {'itemprop':'ratingCount'}).text.replace(',',''))
            # utilities.extract_tags(score_tag.find_all())
            score_point = score_tag.find('span',{'itemprop':'ratingValue'}).text
            try:
                media_info[u'score'] = (decimal.Decimal(score_point), num_users)
            except (InvalidOperation, AttributeError) :
                score_tag = media_page_original.find('span',{'itemprop':'ratingValue'})
                media_info[u'score'] = (decimal.Decimal(score_tag.text), num_users)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            rank_tag = [x for x in media_page.select('span.dark_text') if 'Ranked:' in x.text][0]
            ranking = (
                rank_tag.parent.text.split(':')[1].replace(',', '').split('#')[1].split()[0]
                .strip())
            media_info[u'rank'] = int(ranking)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            try:
                # find popularity html-tag
                popularity_tag = info_panel_first.find(text=u'Popularity:').parent.parent
                utilities.extract_tags(popularity_tag.find_all())
                # format popularity
                popularity = popularity_tag.text.strip()[1:].replace(u',', '')
                if '#' in popularity:
                    popularity = popularity.split('#')[1].split()[0]
                # set into media info
                media_info[u'popularity'] = int(popularity)
            except AttributeError :
                rank_tag = filter(lambda x: 'Popularity' in x.text,
                                  media_page_original.find_all('span', {'class':'dark_text'}))[0].parent
                media_info[u'popularity'] = int(rank_tag.text.split('#')[-1].strip())
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            members_tag = [
                x for x in media_page.select('span.dark_text')
                if 'Members:' in x.text][0]
            members = members_tag.parent.text.split(':')[1].strip().replace(',', '')
            media_info[u'members'] = int(members)

        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            fav_tag = [x for x in media_page.select('span.dark_text') if 'Favorites:' in x.text][0]
            favorites = fav_tag.parent.text.split(':')[1].strip().replace(',', '')
            media_info[u'favorites'] = int(favorites)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return media_info

    def parse_related_media(self, media_page):
        """Parses the DOM and returns related media.

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

    def parse(self, media_page, media_page_original=None):
        """Parses the DOM and returns media attributes in the main-content area.

        :type media_page: :class:`bs4.BeautifulSoup`
        :param media_page: MAL media page's DOM

        :type media_page: :class:`bs4.BeautifulSoup`
        :param media_page: MAL media page's DOM unclean

        :rtype: dict
        :return: media attributes.

        """
        media_info = self.parse_sidebar(media_page, media_page_original)

        try:
            media_info[u'synopsis'] = media_page.find('span', {'itemprop': 'description'}).text
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            related_title = media_page.find(u'h2', text=u'Related ' + self.__class__.__name__)
            if related_title:
                related_elt = related_title.parent
                utilities.extract_tags(related_elt.find_all(u'h2'))
                related = {}
                for link in related_elt.find_all(u'a'):
                    href = link.get(u'href').replace(u'http://myanimelist.net', '')
                    if not re.match(r'/(anime|manga)', href):
                        break
                    curr_elt = link.previous_sibling
                    if curr_elt is None:
                        # we've reached the end of the list.
                        break
                    related_type = None
                    while True:
                        if not curr_elt:
                            raise MalformedAnimePageError(self.id, related_elt,
                                                          message="Prematurely reached end of related anime listing")
                        if isinstance(curr_elt, bs4.NavigableString):
                            type_match = re.match(u'(?P<type>[a-zA-Z\ \-]+):', curr_elt)
                            if type_match:
                                related_type = type_match.group(u'type')
                                break
                        curr_elt = curr_elt.previous_sibling
                    title = link.text
                    # parse link: may be manga or anime.
                    href_parts = href.split(u'/')
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
                media_info[u'related'] = related
            else:
                media_info[u'related'] = None

            # check once again using a single function if the first method found none
            if media_info[u'related'] is None:
                media_info[u'related'] = self.parse_related_media(media_page_original)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return media_info

    def parse_stats(self, media_page):
        """Parses the DOM and returns media statistics attributes.

        :type media_page: :class:`bs4.BeautifulSoup`
        :param media_page: MAL media stats page's DOM

        :rtype: dict
        :return: media stats attributes.

        """
        media_info = self.parse_sidebar(media_page)
        verb_progressive = self.consuming_verb + u'ing'
        status_stats = {
            verb_progressive: 0,
            'completed': 0,
            'on_hold': 0,
            'dropped': 0,
            'plan_to_' + self.consuming_verb: 0
        }
        try:
            consuming_elt = media_page.find(u'span', {'class': 'dark_text'}, text=verb_progressive.capitalize())
            if consuming_elt:
                status_stats[verb_progressive] = int(consuming_elt.nextSibling.strip().replace(u',', ''))
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            completed_elt = media_page.find(u'span', {'class': 'dark_text'}, text="Completed:")
            if completed_elt:
                status_stats[u'completed'] = int(completed_elt.nextSibling.strip().replace(u',', ''))
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            on_hold_elt = media_page.find(u'span', {'class': 'dark_text'}, text="On-Hold:")
            if on_hold_elt:
                status_stats[u'on_hold'] = int(on_hold_elt.nextSibling.strip().replace(u',', ''))
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            dropped_elt = media_page.find(u'span', {'class': 'dark_text'}, text="Dropped:")
            if dropped_elt:
                status_stats[u'dropped'] = int(dropped_elt.nextSibling.strip().replace(u',', ''))
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            planning_elt = media_page.find(u'span', {'class': 'dark_text'},
                                           text="Plan to " + self.consuming_verb.capitalize() + ":")
            if planning_elt:
                status_stats[u'plan_to_' + self.consuming_verb] = int(
                    planning_elt.nextSibling.strip().replace(u',', ''))
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        media_info[u'status_stats'] = status_stats

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
            score_stats_header = media_page.find(u'h2', text='Score Stats')
            if score_stats_header:
                score_stats_table = score_stats_header.find_next_sibling(u'table')
                if score_stats_table:
                    score_stats = {}
                    score_rows = score_stats_table.find_all(u'tr')
                    for i in xrange(len(score_rows)):
                        score_value = int(score_rows[i].find(u'td').text)
                        score_stats[score_value] = int(
                            score_rows[i].find(u'small').text.replace(u'(u', '').replace(u' votes)', ''))
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        media_info[u'score_stats'] = score_stats

        return media_info

    def parse_characters(self, character_page, character_page_original=None):
        """Parses the DOM and returns media character attributes in the sidebar.

        :type character_page: :class:`bs4.BeautifulSoup`
        :param character_page: MAL character page's DOM

        :rtype: dict
        :return: character attributes.

        """
        media_info = self.parse_sidebar(character_page, character_page_original)

        try:
            character_title = list(filter(
                lambda x: u'Characters' in x.text,
                character_page.find_all(u'h2'))
            )
            media_info[u'characters'] = {}
            if character_title:
                character_title = character_title[0]
                curr_elt = character_title.find_next_sibling(u'table')
                while curr_elt:
                    curr_row = curr_elt.find(u'tr')
                    # character in second col.
                    character_col = curr_row.find_all(u'td', recursive=False)[1]
                    character_link = character_col.find(u'a')
                    character_name = ' '.join(reversed(character_link.text.split(u', ')))
                    link_parts = character_link.get(u'href').split(u'/')
                    # of the form /character/7373/Holo
                    character = self.session.character(int(link_parts[2])).set({'name': character_name})
                    role = character_col.find(u'small').text
                    media_info[u'characters'][character] = {'role': role}
                    curr_elt = curr_elt.find_next_sibling(u'table')
            if media_info[u'characters'] == {}:
                character_title = filter(lambda x: u'Characters' in x.text, character_page_original.find_all(u'h2'))
                tables = character_title[0].findNextSiblings(u'table')
                for table in tables:
                    # one table only contain one row which contain 2 cell, which are photo , text
                    # get second cell
                    character_col = table.find_all('td')[1]
                    # find link in that cell
                    character_link = character_col.find(u'a')
                    # find char name and reverse it
                    character_name = ' '.join(reversed(character_link.text.split(u', ')))
                    # get role which written in small-tag
                    role = character_col.find('small').text
                    # get link and split with splash
                    # of the form /character/7373/Holo
                    link_parts = character_link.get(u'href').split(u'/')
                    # create object
                    character = self.session.character(int(link_parts[2])).set({'name': character_name})
                    media_info[u'characters'][character] = {'role': role}
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return media_info

    def load(self):
        """Fetches the MAL media page and sets the current media's attributes.

        :rtype: :class:`.Media`
        :return: current media object.

        """
        media_page = self.session.session.get(
            u'http://myanimelist.net/' + self.__class__.__name__.lower() + u'/' + str(self.id)).text
        media_page_original = bs4.BeautifulSoup(media_page,'lxml')
        self.set(self.parse(utilities.get_clean_dom(media_page), media_page_original))
        return self

    def load_stats(self):
        """Fetches the MAL media statistics page and sets the current media's statistics attributes.

        :rtype: :class:`.Media`
        :return: current media object.

        """
        stats_page = self.session.session.get(u'http://myanimelist.net/' + self.__class__.__name__.lower() + u'/' + str(
            self.id) + u'/' + utilities.urlencode(self.title) + u'/stats').text
        self.set(self.parse_stats(utilities.get_clean_dom(stats_page)))
        return self

    def load_characters(self):
        """Fetches the MAL media characters page and sets the current media's character attributes.

        :rtype: :class:`.Media`
        :return: current media object.

        """
        character_page_url = u'http://myanimelist.net/' + self.__class__.__name__.lower() + u'/' + str(
                self.id) + u'/' + utilities.urlencode(self.title) + u'/characters'
        characters_page = self.session.session.get(character_page_url).text
        characters_page_original = bs4.BeautifulSoup(characters_page,'lxml') 
        self.set(self.parse_characters(utilities.get_clean_dom(characters_page), characters_page_original))
        return self

    @property
    @loadable(u'load')
    def title(self):
        """Media's title.
        """
        return self._title

    @property
    @loadable(u'load')
    def picture(self):
        """URL of media's primary pictures.
        """
        return self._picture

    @property
    @loadable(u'load')
    def alternative_titles(self):
        """Alternative titles dict, with types of titles, e.g. 'Japanese', 'English', or 'Synonyms' as keys, and lists of said alternative titles as values.
        """
        return self._alternative_titles

    @property
    @loadable(u'load')
    def type(self):
        """Type of this media, e.g. 'TV' or 'Manga' or 'Movie'
        """
        return self._type

    @property
    @loadable(u'load')
    def status(self):
        """Publication status, e.g. 'Finished Airing'
        """
        return self._status

    @property
    @loadable(u'load')
    def genres(self):
        """A list of :class:`myanimelist.genre.Genre` objects associated with this media.
        """
        return self._genres

    @property
    @loadable(u'load')
    def score(self):
        """A tuple(2) containing an instance of decimal.Decimal storing the aggregate score, weighted or non-weighted, and an int storing the number of ratings

        """
        return self._score

    @property
    @loadable(u'load')
    def rank(self):
        """Score rank.
        """
        return self._rank

    @property
    @loadable(u'load')
    def popularity(self):
        """Popularity rank.
        """
        return self._popularity

    @property
    @loadable(u'load')
    def members(self):
        """Number of members.
        """
        return self._members

    @property
    @loadable(u'load')
    def favorites(self):
        """Number of users who favourited this media.
        """
        return self._favorites

    @property
    @loadable(u'load')
    def popular_tags(self):
        """Tags dict with :class:`myanimelist.tag.Tag` objects as keys, and the number of tags as values.
        """
        warnings.warn(
            'Popular tags is not available anymore',
            DeprecationWarning
        )
        return self._popular_tags

    @property
    @loadable(u'load')
    def synopsis(self):
        """Media synopsis.
        """
        return self._synopsis

    @property
    @loadable(u'load')
    def related(self):
        """Related media dict, with strings of relation types, e.g. 'Sequel' as keys, and lists containing instances of :class:`.Media` subclasses as values.
        """
        return self._related

    @property
    @loadable(u'load_characters')
    def characters(self):
        """Character dict, with :class:`myanimelist.character.Character` objects as keys, and a dict with attributes of this role, e.g. 'role': 'Main' as values.
        """
        return self._characters

    @property
    @loadable(u'load_stats')
    def status_stats(self):
        """Status statistics dict, with strings of statuses, e.g. 'on_hold' as keys, and an int number of users as values.
        """
        return self._status_stats

    @property
    @loadable(u'load_stats')
    def score_stats(self):
        """Score statistics dict, with int scores from 1-10 as keys, and an int number of users as values.
        """
        return self._score_stats
