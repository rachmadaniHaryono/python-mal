#!/usr/bin/python
# -*- coding: utf-8 -*-
import utilities
from base import Base, MalformedPageError, InvalidBaseError, loadable


class MalformedPersonPageError(MalformedPageError):
    pass


class InvalidPersonError(InvalidBaseError):
    pass


class Person(Base):
    def __init__(self, session, person_id):
        super(Person, self).__init__(session)
        self.id = person_id
        if not isinstance(self.id, int) or int(self.id) < 1:
            raise InvalidPersonError(self.id)
        self._name = None

        self._voice_acting_roles = None
        self._staff_positions = None
        self._published_manga = None

    def load(self):
        """Fetches the MAL person page and sets the current person's attributes.

        :rtype: :class:`.Person`
        :return: Current person object.

        """
        person = self.session.session.get(u'http://myanimelist.net/people/' + str(self.id)).text
        self.set(self.parse(utilities.get_clean_dom(person)))
        return self

    def load_pictures(self):
        """Fetches the MAL person pictures page and sets the current character's pictures attributes.

        :rtype: :class:`.Person`
        :return: Current person object.

        """
        person = self.session.session.get(
            u'http://myanimelist.net/person/' + str(self.id) + u'/' + utilities.urlencode(
                self.name) + u'/pictures').text
        self.set(self.parse_pictures(utilities.get_clean_dom(person)))
        return self

    def parse(self, person_page):
        """Parses the DOM and returns person attributes in the main-content area.

        :type character_page: :class:`bs4.BeautifulSoup`
        :param character_page: MAL person page's DOM

        :rtype: dict
        :return: Person attributes.

        """
        person_info = self.parse_sidebar(person_page)

        def fix_name(name):
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

        # parsing person name
        try:
            temp_name = person_page.select('div#contentWrapper h1.h1')[0].text
            person_info[u'name'] = fix_name(temp_name)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        # parsing person role in anime
        try:
            ''' # Fail with css selector
            css_selector = 'div#contentWrapper div#content table tbody tr td table tr tbody tr'
            va_roles_tags = person_page.select(css_selector)[0]
            '''
            table_sibling = [tag for tag in person_page.select('div.normal_header') if 'Voice Acting Roles' in tag.text][0]
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
                char_tag = [xx for xx in a_tags if '/anime/' in xx.get('href')][0]
                # ie '/character/24502/Yuzuru_Otonashi'
                character_id = int(char_tag.get('href').split('/')[2])
                character_name = fix_name(char_tag.text)
                character_obj = self.session.character(character_id).set({'name': character_name})

                # find the for the said character ie 'main'
                role_tag = va_tag.find_all('td')[2].find('div').text.strip()

                # create a dict which will be merged into va_roles dict
                va_roles[anime_obj] = {character_obj: role_tag}

            # add as person attribute
            person_info[u'voice_acting_roles'] = va_roles

        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return person_info

    def parse_sidebar(self, person_page):
        """Parses the DOM and returns person attributes in the sidebar.

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
        """Parses the DOM and returns person pictures attributes.

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
        return self._name

    @property
    @loadable(u'load')
    def voice_acting_roles(self):
        return self._voice_acting_roles
