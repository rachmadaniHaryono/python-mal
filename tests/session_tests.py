#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase
import os
from nose.plugins.attrib import attr

import myanimelist.session
import myanimelist.anime

@attr('credentials')
class testSessionClass(TestCase):
    @classmethod
    def setUpClass(self):
        # see if our environment has credentials.
        if 'MAL_USERNAME' and 'MAL_PASSWORD' in os.environ:
            self.username = os.environ['MAL_USERNAME']
            self.password = os.environ['MAL_PASSWORD']
        else:
            # rely on a flat textfile in project root.
            with open('credentials.txt', 'r') as cred_file:
                line = cred_file.read().strip().split('\n')[0]
                self.username, self.password = line.strip().split(',')

        self.session = myanimelist.session.Session(self.username, self.password)
        self.logged_in_session = myanimelist.session.Session(self.username, self.password).login()
        self.fake_session = myanimelist.session.Session('no-username', 'no-password')

    def testLoggedIn(self):
        self.assertFalse(self.fake_session.logged_in())
        self.fake_session.login()
        self.assertFalse(self.fake_session.logged_in())
        self.assertFalse(self.session.logged_in())
        self.assertTrue(self.logged_in_session.logged_in())

    def testLogin(self):
        self.assertFalse(self.session.logged_in())
        self.session.login()
        self.assertTrue(self.session.logged_in())

    def testAnime(self):
        self.assertIsInstance(self.session.anime(1), myanimelist.anime.Anime)
