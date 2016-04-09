#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Module for media tag."""

try:
    from base import Base, MalformedPageError, InvalidBaseError
except ImportError:
    from .base import Base, MalformedPageError, InvalidBaseError

class MalformedTagPageError(MalformedPageError):
    pass


class InvalidTagError(InvalidBaseError):
    pass


class Tag(Base):
    _id_attribute = "name"

    def __init__(self, session, name):
        super(Tag, self).__init__(session)
        self.name = name
        if not isinstance(self.name, unicode) or len(self.name) < 1:
            raise InvalidTagError(self.name)

    def load(self):
        # TODO
        pass
