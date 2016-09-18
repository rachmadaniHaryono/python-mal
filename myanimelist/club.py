#!/usr/bin/python
# -*- coding: utf-8 -*-
"""module for myanimelist user."""

try:
    from base import Base, MalformedPageError, InvalidBaseError, loadable
except ImportError:
    from .base import Base, MalformedPageError, InvalidBaseError, loadable


class MalformedClubPageError(MalformedPageError):
    pass


class InvalidClubError(InvalidBaseError):
    pass


class Club(Base):
    def __init__(self, session, club_id):
        super(Club, self).__init__(session)
        self.id = club_id
        if not isinstance(self.id, int) or int(self.id) < 1:
            raise InvalidClubError(self.id)
        self._name = None
        self._num_members = None

    def load(self):
        # TODO
        pass

    @property
    @loadable('load')
    def name(self):
        return self._name

    @property
    @loadable('load')
    def num_members(self):
        return self._num_members
