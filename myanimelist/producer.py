#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from . import utilities
from .base import Base, MalformedPageError, InvalidBaseError, loadable


class MalformedProducerPageError(MalformedPageError):
    pass


class InvalidProducerError(InvalidBaseError):
    pass


class Producer(Base):
    def __init__(self, session, producer_id):
        super(Producer, self).__init__(session)
        self.id = producer_id
        if not isinstance(self.id, int) or int(self.id) < 1:
            raise InvalidProducerError(self.id)
        self._name = None

    def load(self):
        # TODO
        pass

    @property
    @loadable('load')
    def name(self):
        return self._name
