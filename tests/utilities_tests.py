#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase
from datetime import date

try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import myanimelist.session
from myanimelist import utilities


class TestParseProfileDate(TestCase):
    """test to date parser."""

    def test_normal_input(self):
        """test the correct input."""
        txt = 'May 10, 2016'
        res = utilities.parse_profile_date(txt)
        self.assertIsInstance(res, date)
        self.assertEqual(res, date(2016, 5, 10))

class TestIndexContainingSubstring(TestCase):
    """test index_containing_substring method."""

    def test_normal_input(self):
        """test the normal input."""
        l = ['the cat ate the mouse','the tiger ate the chicken','the horse ate the straw']
        res = utilities.index_containing_substring(l, 'tiger')
        self.assertIsInstance(res, int)
        self.assertEqual(res, 1)

        l = [
            'Club Stats',
            'Members: 4',
            'Pictures: 2',
            'Category: Anime',
            'Created: May 10, 2016',
            'Club Officers',
            '         Otaku91 PSKING snake18011992 (Creator)',
            'Club TypeThis is a private club. Members...'
        ]
        res = utilities.index_containing_substring(l, 'Club Type')
        self.assertEqual(res, 7)
        self.assertIsInstance(res, int)
