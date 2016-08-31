#!/usr/bin/python
# -*- coding: utf-8 -*-
"""module for media tag."""

try:
    from base import Base, MalformedPageError, InvalidBaseError
except ImportError:
    from .base import Base, MalformedPageError, InvalidBaseError


class MalformedTagPageError(MalformedPageError):
    """Error raised for invalid tag page."""

    pass


class InvalidTagError(InvalidBaseError):
    """Error raise when tag is invalid."""

    pass


class Tag(Base):
    """tag for myanimelist media."""

    _id_attribute = "name"

    def __init__(self, session, name):
        """init func."""
        super(Tag, self).__init__(session)
        self.name = name
        is_name_text = isinstance(self.name, str)
        if not(is_name_text) or len(self.name) < 1:
            raise InvalidTagError(self.name)

    def load(self):
        """load func."""
        # TODO
        pass
