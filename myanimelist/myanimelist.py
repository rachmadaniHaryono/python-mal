#!/usr/bin/python
# -*- coding: utf-8 -*-
"""myanimelist module."""

try:
    import http.client as client_
except ImportError:
    import httplib as client_


def patch_http_response_read(func):
    """cause httplib to return the partial response from a server.

    it is in case the read fails to be complete.
    """
    def inner(*args):
        try:
            return func(*args)
        except client_.IncompleteRead as e:
            return e.partial

    return inner


client_.HTTPResponse.read = patch_http_response_read(client_.HTTPResponse.read)
