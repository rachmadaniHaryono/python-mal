#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import utilities
from .base import Base, Error, loadable
from . import media_list


class AnimeList(media_list.MediaList):
    __id_attribute = "username"

    def __init__(self, session, user_name):
        super(AnimeList, self).__init__(session, user_name)

    @property
    def type(self):
        return "anime"

    @property
    def verb(self):
        return "watch"

    def parse_entry_media_attributes(self, soup):
        attributes = super(AnimeList, self).parse_entry_media_attributes(soup)

        try:
            attributes['episodes'] = int(soup.find('.//series_episodes').text)
        except ValueError:
            attributes['episodes'] = None
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return attributes

    def parse_entry(self, soup):
        anime, entry_info = super(AnimeList, self).parse_entry(soup)

        try:
            entry_info['episodes_watched'] = int(soup.find('.//my_watched_episodes').text)
        except ValueError:
            entry_info['episodes_watched'] = 0
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            entry_info['rewatching'] = bool(soup.find('.//my_rewatching').text)
        except ValueError:
            entry_info['rewatching'] = False
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            entry_info['episodes_rewatched'] = int(soup.find('.//my_rewatching_ep').text)
        except ValueError:
            entry_info['episodes_rewatched'] = 0
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return anime, entry_info

    def parse_section_columns(self, columns):
        column_names = super(AnimeList, self).parse_section_columns(columns)
        for i, column in enumerate(columns):
            if 'Type' in column.text:
                column_names['type'] = i
            elif 'Progress' in column.text:
                column_names['progress'] = i
            elif 'Tags' in column.text:
                column_names['tags'] = i
            elif 'Started' in column.text:
                column_names['started'] = i
            elif 'Finished' in column.text:
                column_names['finished'] = i
        return column_names
