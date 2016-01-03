#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from . import utilities
from .base import Base, MalformedPageError, InvalidBaseError, loadable


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
        # TODO
        pass

    @property
    @loadable('load')
    def name(self):
        return self._name
