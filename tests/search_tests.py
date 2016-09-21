#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase

import myanimelist.session
from myanimelist.manga import Manga


class TestSearchMethod(TestCase):
    """test search method."""

    @classmethod
    def setUpClass(self):
        """set up class."""
        self.session = myanimelist.session.Session()

    def test_empty_string_mode_all(self):
        """test empty string mode all."""
        with self.assertRaises(ValueError):
            self.session.search('')

    def test_normal_input(self):
        """test normal input."""
        res = self.session.search('main')
        self.assertGreater(len(res), 0)

    def test_not_exist_mode(self):
        """test random mode."""
        with self.assertRaises(ValueError):
            self.session.search('main', mode='random_words')

    def test_not_yet_implemented_mode(self):
        """test mode, which is not yet implemented."""
        with self.assertRaises(NotImplementedError):
            self.session.search('main', mode='featured')

    def test_no_result(self):
        """test when no result from search."""
        """NOTE: myanimelist will give result even if random string is given.
        if any url known which can give no result, test it here."""
        pass

    def test_single_manga_bug(self):
        """test when searching for 'beebop', it only give one manga.

        it is different when searching directly through the browser.
        """
        res = self.session.search('beebop')
        res_manga = [x for x in res if isinstance(x, Manga)]
        self.assertGreater(len(res_manga), 1)

        # sort result by type
        res_di = {}
        for x in res:
            if type(x) not in res_di:
                res_di[type(x)] = [x]
            else:
                res_di[type(x)].append(x)
        for x in res_di:
            self.assertGreater(len(res_di[x]), 1)

