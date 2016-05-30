#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import re

from . import utilities
from . import media
from .base import loadable


class MalformedAnimePageError(media.MalformedMediaPageError):
    """Indicates that an anime-related page on MAL has irreparably broken markup in some way.
    """
    pass


class InvalidAnimeError(media.InvalidMediaError):
    """Indicates that the anime requested does not exist on MAL.
    """
    pass


class Anime(media.Media):
    """Primary interface to anime resources on MAL.
    """
    _status_terms = [
        'Unknown',
        'Currently Airing',
        'Finished Airing',
        'Not yet aired'
    ]
    _consuming_verb = "watch"

    def __init__(self, session, anime_id):
        """Creates a new instance of Anime.

        :type session: :class:`myanimelist.session.Session`
        :param session: A valid MAL session
        :type anime_id: int
        :param anime_id: The desired anime's ID on MAL

        :raises: :class:`.InvalidAnimeError`

        """
        if not isinstance(anime_id, int) or int(anime_id) < 1:
            raise InvalidAnimeError(anime_id)
        super(Anime, self).__init__(session, anime_id)
        self._episodes = None
        self._aired = None
        self._producers = None
        self._duration = None
        self._rating = None
        self._voice_actors = None
        self._staff = None

    def parse_sidebar(self, anime_page):
        """Parses the DOM and returns anime attributes in the sidebar.

        :type anime_page: :class:`lxml.html.HtmlElement`
        :param anime_page: MAL anime page's DOM

        :rtype: dict
        :return: anime attributes

        :raises: :class:`.InvalidAnimeError`, :class:`.MalformedAnimePageError`
        """
        # if MAL says the series doesn't exist, raise an InvalidAnimeError.
        if not self._validate_page(anime_page):
            raise InvalidAnimeError(self.id)

        title_tag = anime_page.xpath(".//div[@id='contentWrapper']//h1//span")
        if len(title_tag) == 0:
            raise MalformedAnimePageError(self.id, anime_page.text, message="Could not find title div")

        anime_info = super(Anime, self).parse_sidebar(anime_page)
        info_panel_first = None

        try:
            container = utilities.css_select("#content", anime_page)
            if container is None:
                raise MalformedAnimePageError(self.id, anime_page.text, message="Could not find the info table")

            info_panel_first = container[0].find(".//table/tr/td")
            temp = info_panel_first.xpath(".//div/span[text()[contains(.,'Episodes:')]]")
            if len(temp) == 0:
                raise Exception("Couldn't find episode tag.")
            episode_tag = temp[0].getparent().xpath(".//text()")[-1]
            anime_info['episodes'] = int(episode_tag.strip()) if episode_tag.strip() != 'Unknown' else 0
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            temp = info_panel_first.xpath(".//div/span[text()[contains(.,'Aired:')]]")
            if len(temp) == 0:
                raise Exception("Couldn't find aired tag.")
            aired_tag = temp[0].getparent().xpath(".//text()")[2]
            aired_parts = aired_tag.strip().split(' to ')
            if len(aired_parts) == 1:
                # this aired once.
                try:
                    aired_date = utilities.parse_profile_date(aired_parts[0],
                                                              suppress=self.session.suppress_parse_exceptions)
                except ValueError:
                    raise MalformedAnimePageError(self.id, aired_parts[0], message="Could not parse single air date")
                anime_info['aired'] = (aired_date,)
            else:
                # two airing dates.
                try:
                    air_start = utilities.parse_profile_date(aired_parts[0],
                                                             suppress=self.session.suppress_parse_exceptions)
                except ValueError:
                    raise MalformedAnimePageError(self.id, aired_parts[0],
                                                  message="Could not parse first of two air dates")
                try:
                    air_end = utilities.parse_profile_date(aired_parts[1],
                                                           suppress=self.session.suppress_parse_exceptions)
                except ValueError:
                    raise MalformedAnimePageError(self.id, aired_parts[1],
                                                  message="Could not parse second of two air dates")
                anime_info['aired'] = (air_start, air_end)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            temp = info_panel_first.xpath(".//div/span[text()[contains(.,'Producers:')]]")
            if len(temp) == 0:
                raise Exception("Couldn't find producers tag.")
            producers_tags = temp[0].getparent().xpath(".//a")
            anime_info['producers'] = []
            for producer_link in producers_tags:
                if producer_link.text == 'add some':
                    # MAL is saying "None found, add some".
                    break
                link_parts = producer_link.get('href').split('p=')
                # of the form: /anime.php?p=14
                if len(link_parts) > 1:
                    anime_info['producers'].append(
                            self.session.producer(int(link_parts[1])).set({'name': producer_link.text}))
                else:
                    # of the form: /anime/producer/65
                    link_parts = producer_link.get('href').split('/')
                    anime_info['producers'].append(
                            self.session.producer(int(link_parts[-2])).set({"name": producer_link.text}))
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            temp = info_panel_first.xpath(".//div/span[text()[contains(.,'Duration:')]]")
            if len(temp) == 0:
                raise Exception("Couldn't find duration tag.")
            duration_tag = temp[0].xpath("../text()")[-1]
            anime_info['duration'] = duration_tag.strip()
            duration_parts = [part.strip() for part in anime_info['duration'].split('.')]
            duration_mins = 0
            for part in duration_parts:
                part_match = re.match('(?P<num>[0-9]+)', part)
                if not part_match:
                    continue
                part_volume = int(part_match.group('num'))
                if part.endswith('hr'):
                    duration_mins += part_volume * 60
                elif part.endswith('min'):
                    duration_mins += part_volume
            anime_info['duration'] = datetime.timedelta(minutes=duration_mins)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            temp = info_panel_first.xpath(".//div/span[text()[contains(.,'Rating:')]]")
            if len(temp) == 0:
                raise Exception("Couldn't find duration tag.")
            rating_tag = temp[0].xpath(".//text()")[-1]
            anime_info['rating'] = rating_tag.strip()
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return anime_info

    def parse_characters(self, character_page):
        """Parses the DOM and returns anime character attributes in the sidebar.

        :type character_page: :class:`lxml.html.HtmlElement`
        :param character_page: MAL anime character page's DOM

        :rtype: dict
        :return: anime character attributes

        :raises: :class:`.InvalidAnimeError`, :class:`.MalformedAnimePageError`

        """
        anime_info = self.parse_sidebar(character_page)

        try:
            temp = character_page.xpath(".//h2[text()[contains(.,'Characters')]]/following-sibling::table[1]")

            anime_info['characters'] = {}
            anime_info['voice_actors'] = {}

            if len(temp) != 0:
                curr_elt = temp[0]
                while curr_elt is not None:
                    if curr_elt.tag != 'table':
                        break
                    curr_row = curr_elt.find('.//tr')
                    temp = curr_row.findall("./td")
                    # we got to the staff part, todo: fix the sibling part. this is ugly
                    if len(temp) != 3:
                        break
                    (_, character_col, va_col) = temp

                    character_link = character_col.find('.//a')
                    character_name = ' '.join(reversed(character_link.text.split(', ')))
                    link_parts = character_link.get('href').split('/')
                    # of the form /character/7373/Holo
                    character = self.session.character(int(link_parts[2])).set({'name': character_name})
                    role = character_col.find('.//small').text
                    character_entry = {'role': role, 'voice_actors': {}}

                    va_table = va_col.find('.//table')
                    if va_table is not None:
                        for row in va_table.findall("tr"):
                            va_info_cols = row.findall('td')
                            if not va_info_cols or len(va_info_cols) == 0:
                                # don't ask me why MAL has an extra blank table row i don't know!!!
                                continue

                            va_info_col = va_info_cols[0]
                            va_link = va_info_col.find('.//a')
                            if va_link is not None:
                                va_name = ' '.join(reversed(va_link.text.split(', ')))
                                link_parts = va_link.get('href').split('/')
                                # of the form /people/70/Ami_Koshimizu
                                person = self.session.person(int(link_parts[2])).set({'name': va_name})
                                language = va_info_col.find('.//small').text
                                anime_info['voice_actors'][person] = {'role': role, 'character': character,
                                                                      'language': language}
                                character_entry['voice_actors'][person] = language

                    anime_info['characters'][character] = character_entry
                    temp = curr_elt.xpath("./following-sibling::table[1]")
                    if len(temp) != 0:
                        curr_elt = temp[0]
                    else:
                        curr_elt = None
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            temp = character_page.xpath(".//h2[text()[contains(.,'Staff')]]/following-sibling::table[1]")
            anime_info['staff'] = {}
            if len(temp) != 0:
                staff_table = temp[0]
                for row in staff_table.findall('.//tr'):
                    # staff info in second col.
                    info = row.find('./td[2]')
                    staff_link = info.find('.//a')
                    if staff_link is not None:
                        staff_name = ' '.join(reversed(staff_link.text.split(', ')))
                        link_parts = staff_link.get('href').split('/')
                        # of the form /people/1870/Miyazaki_Hayao
                        person = self.session.person(int(link_parts[-2])).set({'name': staff_name})
                        # staff role(s).
                        smallTag = info.find('.//small')
                        if smallTag is not None:
                            anime_info['staff'][person] = set(smallTag.text.split(', '))
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return anime_info

    @property
    @loadable('load')
    def episodes(self):
        """The number of episodes in this anime. If undetermined, is None, otherwise > 0.
        """
        return self._episodes

    @property
    @loadable('load')
    def aired(self):
        """A tuple(2) containing up to two :class:`datetime.date` objects representing the start and end dates of this anime's airing.

          Potential configurations:

            None -- Completely-unknown airing dates.

            (:class:`datetime.date`, None) -- Anime start date is known, end date is unknown.

            (:class:`datetime.date`, :class:`datetime.date`) -- Anime start and end dates are known.

        """
        return self._aired

    @property
    @loadable('load')
    def producers(self):
        """A list of :class:`myanimelist.producer.Producer` objects involved in this anime.
        """
        return self._producers

    @property
    @loadable('load')
    def duration(self):
        """The duration of an episode of this anime as a :class:`datetime.timedelta`.
        """
        return self._duration

    @property
    @loadable('load')
    def rating(self):
        """The MPAA rating given to this anime.
        """
        return self._rating

    @property
    @loadable('load_characters')
    def voice_actors(self):
        """A voice actors dict with :class:`myanimelist.person.Person` objects of the voice actors as keys, and dicts containing info about the roles played, e.g. {'role': 'Main', 'character': myanimelist.character.Character(1)} as values.
        """
        return self._voice_actors

    @property
    @loadable('load_characters')
    def staff(self):
        """A staff dict with :class:`myanimelist.person.Person` objects of the staff members as keys, and lists containing the various duties performed by staff members as values.
        """
        return self._staff
