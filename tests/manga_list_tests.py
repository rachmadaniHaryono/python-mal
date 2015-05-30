#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase
import datetime

import myanimelist.session
import myanimelist.media_list
import myanimelist.manga_list


class testMangaListClass(TestCase):
    @classmethod
    def setUpClass(self):
        self.session = myanimelist.session.Session()

        self.shal = self.session.manga_list(u'shaldengeki')
        self.tomoyo_after = self.session.manga(3941)
        self.fma = self.session.manga(25)

        self.pl = self.session.manga_list(u'PaperLuigi')
        self.to_love_ru = self.session.manga(671)
        self.amnesia = self.session.manga(15805)
        self.sao = self.session.manga(21479)

        self.josh = self.session.manga_list(u'angryaria')
        self.juicy = self.session.manga(13250)
        self.tsubasa = self.session.manga(1147)
        self.jojo = self.session.manga(1706)

        self.threger = self.session.manga_list(u'threger')

    def testNoUsernameInvalidMangaList(self):
        with self.assertRaises(TypeError):
            self.session.manga_list()

    def testNonexistentUsernameInvalidMangaList(self):
        with self.assertRaises(myanimelist.media_list.InvalidMediaListError):
            self.session.manga_list(u'aspdoifpjsadoifjapodsijfp').load()

    def testUserValid(self):
        assert isinstance(self.shal, myanimelist.manga_list.MangaList)

    def testUsername(self):
        self.assertEqual(self.shal.username, u'shaldengeki')
        self.assertEqual(self.josh.username, u'angryaria')

    def testType(self):
        self.assertEqual(self.shal.type, u'manga')

    def testList(self):
        assert isinstance(self.shal.list, dict)
        self.assertEqual(len(self.shal), 2)
        self.assertIn(self.tomoyo_after, self.shal)
        self.assertIn(self.fma, self.shal)
        self.assertEqual(self.shal[self.tomoyo_after][u'status'], u'Completed')
        self.assertEqual(self.shal[self.fma][u'status'], u'Dropped')
        self.assertEqual(self.shal[self.tomoyo_after][u'score'], 9)
        self.assertEqual(self.shal[self.fma][u'score'], 6)
        self.assertEqual(self.shal[self.tomoyo_after][u'chapters_read'], 4)
        self.assertEqual(self.shal[self.fma][u'chapters_read'], 73)
        self.assertEqual(self.shal[self.tomoyo_after][u'volumes_read'], 1)
        self.assertEqual(self.shal[self.fma][u'volumes_read'], 18)
        self.assertIsNone(self.shal[self.tomoyo_after][u'started'])
        self.assertIsNone(self.shal[self.fma][u'started'])
        self.assertIsNone(self.shal[self.tomoyo_after][u'finished'])
        self.assertIsNone(self.shal[self.fma][u'finished'])

        assert isinstance(self.pl.list, dict)
        self.assertGreaterEqual(len(self.pl), 45)
        self.assertIn(self.to_love_ru, self.pl)
        self.assertIn(self.amnesia, self.pl)
        self.assertIn(self.sao, self.pl)
        self.assertEqual(self.pl[self.to_love_ru][u'status'], u'Completed')
        assert self.pl[self.amnesia][
                                                                           u'status'] == u'On-Hold'
        self.assertEqual(self.pl[self.sao][u'status'], u'Plan to Read')
        self.assertEqual(self.pl[self.to_love_ru][u'score'], 6)
        self.assertIsNone(self.pl[self.amnesia][u'score'])
        self.assertIsNone(self.pl[self.sao][u'score'])
        self.assertEqual(self.pl[self.to_love_ru][u'chapters_read'], 162)
        self.assertEqual(self.pl[self.amnesia][u'chapters_read'], 9)
        self.assertEqual(self.pl[self.sao][u'chapters_read'], 0)
        self.assertEqual(self.pl[self.to_love_ru][u'volumes_read'], 18)
        self.assertEqual(self.pl[self.amnesia][u'volumes_read'], 0)
        self.assertEqual(self.pl[self.sao][u'volumes_read'], 0)
        self.assertEqual(self.pl[self.to_love_ru][u'started'], datetime.date(year=2011, month=9, day=8))
        self.assertEqual(self.pl[self.amnesia][u'started'], datetime.date(year=2010, month=6, day=27))
        self.assertEqual(self.pl[self.sao][u'started'], datetime.date(year=2012, month=9, day=24))
        self.assertEqual(self.pl[self.to_love_ru][u'finished'], datetime.date(year=2011, month=9, day=16))
        self.assertIsNone(self.pl[self.amnesia][u'finished'])
        self.assertIsNone(self.pl[self.sao][u'finished'])

        self.assertIsInstance(self.josh.list, dict)
        self.assertGreaterEqual(len(self.josh), 151)
        self.assertIn(self.juicy, self.josh)
        self.assertIn(self.tsubasa, self.josh)
        self.assertIn(self.jojo, self.josh)
        self.assertEqual(self.josh[self.juicy][u'status'], u'Completed')
        self.assertEqual(self.josh[self.tsubasa][u'status'], u'Dropped')
        self.assertEqual(self.josh[self.jojo][u'status'], u'Plan to Read')
        self.assertEqual(self.josh[self.juicy][u'score'], 6)
        self.assertEqual(self.josh[self.tsubasa][u'score'], 6)
        self.assertIsNone(self.josh[self.jojo][u'score'])
        self.assertEqual(self.josh[self.juicy][u'chapters_read'], 33)
        self.assertEqual(self.josh[self.tsubasa][u'chapters_read'], 27)
        self.assertEqual(self.josh[self.jojo][u'chapters_read'], 0)
        self.assertEqual(self.josh[self.juicy][u'volumes_read'], 2)
        self.assertEqual(self.josh[self.tsubasa][u'volumes_read'], 0)
        self.assertEqual(self.josh[self.jojo][u'volumes_read'], 0)
        self.assertIsNone(self.josh[self.juicy][u'started'])
        self.assertIsNone(self.josh[self.tsubasa][u'started'])
        self.assertEqual(self.josh[self.jojo][u'started'], datetime.date(year=2010, month=9, day=16))
        self.assertIsNone(self.josh[self.juicy][u'finished'])
        self.assertIsNone(self.josh[self.tsubasa][u'finished'])
        self.assertIsNone(self.josh[self.jojo][u'finished'])

        self.assertIsInstance(self.threger.list, dict)
        self.assertEqual(len(self.threger), 0)

    def testStats(self):
        self.assertIsInstance(self.shal.stats, dict)
        self.assertGreater(len(self.shal.stats), 0)
        self.assertEqual(self.shal.stats[u'reading'], 0)
        self.assertEqual(self.shal.stats[u'completed'], 1)
        assert self.shal.stats[
                                                                                               u'on_hold'] == 0
        self.assertEqual(self.shal.stats[u'dropped'], 1)
        self.assertEqual(self.shal.stats[u'plan_to_read'], 0)
        self.assertEqual(float(self.shal.stats[u'days_spent']), 0.95)

        self.assertIsInstance(self.pl.stats, dict)
        self.assertGreater(len(self.pl.stats), 0)
        self.assertGreaterEqual(self.pl.stats[u'reading'], 0)
        self.assertGreaterEqual(self.pl.stats[u'completed'], 16)
        assert self.pl.stats[
                                                                                            u'on_hold'] >= 0
        self.assertGreaterEqual(self.pl.stats[u'dropped'], 0)
        self.assertGreaterEqual(self.pl.stats[u'plan_to_read'], 0)
        self.assertGreaterEqual(float(self.pl.stats[u'days_spent']), 10.28)

        self.assertIsInstance(self.josh.stats, dict)
        self.assertGreater(len(self.josh.stats), 0)
        self.assertGreaterEqual(self.josh.stats[u'reading'], 0)
        self.assertGreaterEqual(self.josh.stats[u'completed'], 53)
        self.assertGreaterEqual(self.josh.stats[u'on_hold'], 0)
        self.assertGreaterEqual(self.josh.stats[u'dropped'], 0)
        self.assertGreaterEqual(self.josh.stats[u'plan_to_read'], 0)
        self.assertGreaterEqual(float(self.josh.stats[u'days_spent']), 25.41)

        self.assertIsInstance(self.threger.stats, dict)
        self.assertGreater(len(self.threger.stats), 0)
        self.assertEqual(self.threger.stats[u'reading'], 0)
        self.assertEqual(self.threger.stats[u'completed'], 0)
        self.assertEqual(self.threger.stats[u'on_hold'], 0)
        self.assertEqual(self.threger.stats[u'dropped'], 0)
        self.assertEqual(self.threger.stats[u'plan_to_read'], 0)
        self.assertEqual(float(self.threger.stats[u'days_spent']), 0.00)

    def testSection(self):
        self.assertIsInstance(self.shal.section(u'Completed'), dict)
        self.assertIn(self.tomoyo_after, self.shal.section(u'Completed'))
        self.assertIsInstance(self.pl.section(u'On-Hold'), dict)
        self.assertIn(self.amnesia, self.pl.section(u'On-Hold'))
        self.assertIsInstance(self.josh.section(u'Plan to Read'), dict)
        self.assertIn(self.jojo, self.josh.section(u'Plan to Read'))
        self.assertIsInstance(self.threger.section(u'Reading'), dict)
        self.assertEqual(len(self.threger.section(u'Reading')), 0)
