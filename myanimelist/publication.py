#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Module for mannga publication."""

try:
    from base import Base, MalformedPageError, InvalidBaseError, loadable
except ImportError:
    from .base import Base, MalformedPageError, InvalidBaseError, loadable


class MalformedPublicationPageError(MalformedPageError):
    pass


class InvalidPublicationError(InvalidBaseError):
    pass


class Publication(Base):
    def __init__(self, session, publication_id):
        super(Publication, self).__init__(session)
        self.id = publication_id
        if not isinstance(self.id, int) or int(self.id) < 1:
            raise InvalidPublicationError(self.id)
        self._name = None

    def load(self):
        # TODO
        pass

    @property
    @loadable('load')
    def name(self):
        return self._name
