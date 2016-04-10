#!/usr/bin/python
# -*- coding: utf-8 -*-

import http.client

# causes httplib to return the partial response from a server in case the read fails to be complete.
def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except http.client.IncompleteRead as e:
            return e.partial

    return inner


http.client.HTTPResponse.read = patch_http_response_read(http.client.HTTPResponse.read)
