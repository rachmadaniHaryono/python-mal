#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Module for media tag."""

try:
    from .base import Base, MalformedPageError, InvalidBaseError
except ImportError:
    from .base import Base, MalformedPageError, InvalidBaseError

try:
    unicode
except NameError:
    unicode = str


class MalformedTagPageError(MalformedPageError):
    """Error when parsing tag page."""

    pass


class InvalidTagError(InvalidBaseError):
    """error for invalid tag."""

    pass


class Tag(Base):
    """class for tag obj."""

    _id_attribute = "name"

    def __init__(self, session, name):
        """init function."""
        super(Tag, self).__init__(session)
        self.name = name
        is_name_string = False
        if isinstance(self.name, unicode) or isinstance(self.name, str):
            is_name_string = True
        if not is_name_string or len(self.name) < 1:
            raise InvalidTagError(self.name)

    def load(self):
        """load all information from tag."""
        # TODO
        pass
