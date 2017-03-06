#!/usr/bin/python
# -*- coding: utf-8 -*-
import abc
import functools

from . import utilities
from lxml import html as ht


class Error(Exception):
    """Base exception class that takes a message to display upon raising.
    """

    def __init__(self, message=None):
        """Creates an instance of Error.

        :type message: str
        :param message: A message to display when raising the exception.

        """
        super(Error, self).__init__()
        self.message = message

    def __str__(self):
        return str(self.message) if self.message is not None else ""


class MalformedPageError(Error):
    """Indicates that a page on MAL has broken markup in some way.
    """

    def __init__(self, id, html, message=None):
        super(MalformedPageError, self).__init__(message=message)
        if isinstance(id, str):
            self.id = id
        else:
            self.id = str(id)
        if isinstance(html, str):
            self.html = html
        else:
            if isinstance(html, ht.HtmlElement):
                self.html = html.text
            else:
                self.html = str(html)

    def __str__(self):
        none_str_const = "<none>"
        return "\n".join([
            super(MalformedPageError, self).__str__(),
            "ID: " + self.id if self.id is not None else none_str_const,
            "HTML: " + self.html if self.html is not None else none_str_const
        ])


class InvalidBaseError(Error):
    """Indicates that the particular resource instance requested does not exist on MAL.
    """

    def __init__(self, id, message=None):
        super(InvalidBaseError, self).__init__(message=message)
        self.id = id

    def __str__(self):
        return "\n".join([
            super(InvalidBaseError, self).__str__(),
            "ID: " + str(self.id)
        ])


def loadable(func_name):
    """Decorator for getters that require a load() upon first access.

    :type func_name: function
    :param func_name: class method that requires that load() be called if the class's _attribute value is None

    :rtype: function
    :return: the decorated class method.

    """

    def inner(func):
        cached_name = '_' + func.__name__

        @functools.wraps(func)
        def _decorator(self, *args, **kwargs):
            if getattr(self, cached_name) is None:
                getattr(self, func_name)()
            return func(self, *args, **kwargs)

        return _decorator

    return inner


class Base(object, metaclass=abc.ABCMeta):
    """Abstract base class for MAL resources. Provides autoloading, auto-setting functionality for other MAL objects.
    """

    """Attribute name for primary reference key to this object.
    When an attribute by the name given by _id_attribute is passed into set(), set() doesn't prepend an underscore for load()ing.
    """
    _id_attribute = "id"

    def __repr__(self):
        return "".join([
            "<",
            self.__class__.__name__,
            " ",
            self._id_attribute,
            ": ",
            str(getattr(self, self._id_attribute)),
            ">"
        ])

    def __hash__(self):
        return hash('-'.join([self.__class__.__name__, str(getattr(self, self._id_attribute))]))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and getattr(self, self._id_attribute) == getattr(other,
                                                                                                  other._id_attribute)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __init__(self, session):
        """Create an instance of Base.

        :type session: :class:`myanimelist.session.Session`
        :param session: A valid MAL session.

        """
        self.session = session

    @staticmethod
    def _validate_page(media_page):
        error_tag = media_page.xpath(".//p[@class='error_code'] | .//div[@class='badresult'] | .//div["
                                     "@class='error404']")
        return len(error_tag) is 0

    @abc.abstractmethod
    def load(self):
        """A callback to run before any @loadable attributes are returned.
        """
        pass

    def set(self, attr_dict):
        """Sets attributes of this user object.

        :type attr_dict: dict
        :param attr_dict: Parameters to set, with attribute keys.

        :rtype: :class:`.Base`
        :return: The current object.

        """
        for key in attr_dict:
            if key == self._id_attribute:
                setattr(self, self._id_attribute, attr_dict[key])
            else:
                setattr(self, "_" + key, attr_dict[key])
        return self
