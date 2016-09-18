#!/usr/bin/python
# -*- coding: utf-8 -*-
import abc
import functools
from six import string_types

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
            try:
                self.id = str(id).decode(u'utf-8')
            except AttributeError:
                self.id = str(id)
        if isinstance(html, string_types):
            self.html = html
        else:
            try:
                self.html = str(html).decode(u'utf-8')
            except AttributeError:
                self.html = str(html)

    def __str__(self):
        return "\n".join([
            super(MalformedPageError, self).__str__(),
            "ID: " + self.id,
            "HTML: " + self.html
        ]).encode('utf-8')


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


def with_metaclass(mcls):
    """decorator for metaclass."""
    def decorator(cls):
        body = vars(cls).copy()
        # clean out class body
        body.pop('__dict__', None)
        body.pop('__weakref__', None)
        return mcls(cls.__name__, cls.__bases__, body)
    return decorator


@with_metaclass(abc.ABCMeta)
class Base(object):
    """Abstract base class for MAL resources.

    Provides autoloading, auto-setting functionality for other MAL objects.
    """

    """Attribute name for primary reference key to this object.
    When an attribute by the name given by _id_attribute is passed into set(),
    set() doesn't prepend an underscore for load()ing.
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
        """hash for class."""
        try:
            return hash('-'.join([self.__class__.__name__, unicode(
                getattr(self, self._id_attribute)
            )]))

        except NameError:
            return hash('-'.join([self.__class__.__name__, str(
                getattr(self, self._id_attribute)
            )]))

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
