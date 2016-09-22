#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase
import os
from nose.plugins.attrib import attr

import myanimelist.session
import myanimelist.anime
import myanimelist.character

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


class testLoadFromURLMethod(TestCase):
    """test to check if load from url function properly."""

    @classmethod
    def setUpClass(self):
        """set up class."""
        self.session = myanimelist.session.Session()

    def test_normal_input(self):
        """test normal input."""
        url = 'https://myanimelist.net/character/15264/Maina'
        res = self.session.load_from_url(url)
        self.assertIsInstance(res, myanimelist.character.Character)

    def test_wrong_input(self):
        """test wrong input."""
        url = 'www.google.com'
        with self.assertRaises(ValueError):
            self.session.load_from_url(url)

        url = 'ftp://myanimelist.net/character/15264/Maina'
        with self.assertRaises(ValueError):
            self.session.load_from_url(url)

        url = 'https://youranimelist.net/character/15264/Maina'
        with self.assertRaises(ValueError):
            self.session.load_from_url(url)

        url = 'https://myanimelist.net/blog.php'
        with self.assertRaises(ValueError):
            self.session.load_from_url(url)

    def test_club_input(self):
        """test club url."""
        url = 'https://myanimelist.net/clubs.php?cid=71268'
        self.session.load_from_url(url)

        # wrong format of club input, but similar to other media input
        url = 'https://myanimelist.net/club/71268'
        with self.assertRaises(ValueError):
            self.session.load_from_url(url)

    def test_long_url(self):
        """test if long valid url still can be recognized."""
        url = 'https://myanimelist.net/anime/6116/Mainichi_Kaasan/video'
        res = self.session.load_from_url(url)
        self.assertIsInstance(res, myanimelist.anime.Anime)
