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

    def load(self):
        """Fetches the MAL person page and sets the current person's attributes.

        :rtype: :class:`.Person`
        :return: Current person object.

        """
        person = self.session.session.get(u'http://myanimelist.net/character/' + str(self.id)).text
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
        pass

    def parse_sidebar(self, person_page):
        """Parses the DOM and returns person attributes in the sidebar.

        :type character_page: :class:`bs4.BeautifulSoup`
        :param character_page: MAL person page's DOM

        :rtype: dict
        :return: person attributes

        :raises: :class:`.InvalidCharacterError`, :class:`.MalformedCharacterPageError`
        """
        pass

    def parse_pictures(self, picture_page):
        """Parses the DOM and returns person pictures attributes.

        :type picture_page: :class:`bs4.BeautifulSoup`
        :param picture_page: MAL person pictures page's DOM

        :rtype: dict
        :return: person pictures attributes.

        """
        pass

    @property
    @loadable(u'load')
    def name(self):
        return self._name
