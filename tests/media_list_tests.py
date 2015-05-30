#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase

import myanimelist.session
import myanimelist.media_list


class testMediaListClass(TestCase):
    @classmethod
    def setUpClass(self):
        self.session = myanimelist.session.Session()

    def testCannotInstantiateMediaList(self):
        with self.assertRaises(TypeError):
            myanimelist.media_list.MediaList(self.session, "test_username")
