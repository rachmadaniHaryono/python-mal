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

        self.shal = self.session.manga_list('shaldengeki')
        self.tomoyo_after = self.session.manga(3941)
        self.fma = self.session.manga(25)

        self.pl = self.session.manga_list('PaperLuigi')
        self.to_love_ru = self.session.manga(671)
        self.amnesia = self.session.manga(15805)
        self.sao = self.session.manga(21479)

        self.josh = self.session.manga_list('angryaria')
        self.juicy = self.session.manga(13250)
        self.tsubasa = self.session.manga(1147)
        self.jojo = self.session.manga(1706)

        self.threger = self.session.manga_list('threger')

    def testNoUsernameInvalidMangaList(self):
        with self.assertRaises(TypeError):
            self.session.manga_list()

    def testNonexistentUsernameInvalidMangaList(self):
        with self.assertRaises(myanimelist.media_list.InvalidMediaListError):
            self.session.manga_list('aspdoifpjsadoifjapodsijfp').load()

    def testUserValid(self):
        assert isinstance(self.shal, myanimelist.manga_list.MangaList)

    def testUsername(self):
        self.assertEqual(self.shal.username, 'shaldengeki')
        self.assertEqual(self.josh.username, 'angryaria')

    def testType(self):
        self.assertEqual(self.shal.type, 'manga')

    def testList(self):
        assert isinstance(self.shal.list, dict)
        self.assertEqual(len(self.shal), 2)
        self.assertIn(self.tomoyo_after, self.shal)
        self.assertIn(self.fma, self.shal)
        self.assertEqual(self.shal[self.tomoyo_after]['status'], 'Completed')
        self.assertEqual(self.shal[self.fma]['status'], 'Dropped')
        self.assertEqual(self.shal[self.tomoyo_after]['score'], 9)
        self.assertEqual(self.shal[self.fma]['score'], 6)
        self.assertEqual(self.shal[self.tomoyo_after]['chapters_read'], 4)
        self.assertEqual(self.shal[self.fma]['chapters_read'], 73)
        self.assertEqual(self.shal[self.tomoyo_after]['volumes_read'], 1)
        self.assertEqual(self.shal[self.fma]['volumes_read'], 18)
        self.assertIsNone(self.shal[self.tomoyo_after]['started'])
        self.assertIsNone(self.shal[self.fma]['started'])
        self.assertIsNone(self.shal[self.tomoyo_after]['finished'])
        self.assertIsNone(self.shal[self.fma]['finished'])

        assert isinstance(self.pl.list, dict)
        self.assertGreaterEqual(len(self.pl), 45)
        self.assertIn(self.to_love_ru, self.pl)
        self.assertIn(self.amnesia, self.pl)
        self.assertIn(self.sao, self.pl)
        self.assertEqual(self.pl[self.to_love_ru]['status'], 'Completed')
        assert self.pl[self.amnesia][
                   'status'] == 'On-Hold'
        self.assertEqual(self.pl[self.sao]['status'], 'Plan to Read')
        self.assertEqual(self.pl[self.to_love_ru]['score'], 6)
        self.assertIsNone(self.pl[self.amnesia]['score'])
        self.assertIsNone(self.pl[self.sao]['score'])
        self.assertEqual(self.pl[self.to_love_ru]['chapters_read'], 162)
        self.assertEqual(self.pl[self.amnesia]['chapters_read'], 9)
        self.assertEqual(self.pl[self.sao]['chapters_read'], 0)
        self.assertEqual(self.pl[self.to_love_ru]['volumes_read'], 18)
        self.assertEqual(self.pl[self.amnesia]['volumes_read'], 0)
        self.assertEqual(self.pl[self.sao]['volumes_read'], 0)
        self.assertEqual(self.pl[self.to_love_ru]['started'], datetime.date(year=2011, month=9, day=8))
        self.assertEqual(self.pl[self.amnesia]['started'], datetime.date(year=2010, month=6, day=27))
        self.assertEqual(self.pl[self.sao]['started'], datetime.date(year=2012, month=9, day=24))
        self.assertEqual(self.pl[self.to_love_ru]['finished'], datetime.date(year=2011, month=9, day=16))
        self.assertIsNone(self.pl[self.amnesia]['finished'])
        self.assertIsNone(self.pl[self.sao]['finished'])

        self.assertIsInstance(self.josh.list, dict)
        self.assertGreaterEqual(len(self.josh), 151)
        self.assertIn(self.juicy, self.josh)
        self.assertIn(self.tsubasa, self.josh)
        self.assertIn(self.jojo, self.josh)
        self.assertEqual(self.josh[self.juicy]['status'], 'Completed')
        self.assertEqual(self.josh[self.tsubasa]['status'], 'Dropped')
        self.assertEqual(self.josh[self.jojo]['status'], 'Plan to Read')
        self.assertEqual(self.josh[self.juicy]['score'], 6)
        self.assertEqual(self.josh[self.tsubasa]['score'], 6)
        self.assertIsNone(self.josh[self.jojo]['score'])
        self.assertEqual(self.josh[self.juicy]['chapters_read'], 33)
        self.assertEqual(self.josh[self.tsubasa]['chapters_read'], 27)
        self.assertEqual(self.josh[self.jojo]['chapters_read'], 0)
        self.assertEqual(self.josh[self.juicy]['volumes_read'], 2)
        self.assertEqual(self.josh[self.tsubasa]['volumes_read'], 0)
        self.assertEqual(self.josh[self.jojo]['volumes_read'], 0)
        self.assertIsNone(self.josh[self.juicy]['started'])
        self.assertIsNone(self.josh[self.tsubasa]['started'])
        self.assertEqual(self.josh[self.jojo]['started'], datetime.date(year=2010, month=9, day=16))
        self.assertIsNone(self.josh[self.juicy]['finished'])
        self.assertIsNone(self.josh[self.tsubasa]['finished'])
        self.assertIsNone(self.josh[self.jojo]['finished'])

        self.assertIsInstance(self.threger.list, dict)
        self.assertEqual(len(self.threger), 0)

    def testStats(self):
        self.assertIsInstance(self.shal.stats, dict)
        self.assertGreater(len(self.shal.stats), 0)
        self.assertEqual(self.shal.stats['reading'], 0)
        self.assertEqual(self.shal.stats['completed'], 1)
        assert self.shal.stats[
                   'on_hold'] == 0
        self.assertEqual(self.shal.stats['dropped'], 1)
        self.assertEqual(self.shal.stats['plan_to_read'], 0)
        self.assertEqual(float(self.shal.stats['days_spent']), 0.95)

        self.assertIsInstance(self.pl.stats, dict)
        self.assertGreater(len(self.pl.stats), 0)
        self.assertGreaterEqual(self.pl.stats['reading'], 0)
        self.assertGreaterEqual(self.pl.stats['completed'], 16)
        assert self.pl.stats[
                   'on_hold'] >= 0
        self.assertGreaterEqual(self.pl.stats['dropped'], 0)
        self.assertGreaterEqual(self.pl.stats['plan_to_read'], 0)
        self.assertGreaterEqual(float(self.pl.stats['days_spent']), 10.28)

        self.assertIsInstance(self.josh.stats, dict)
        self.assertGreater(len(self.josh.stats), 0)
        self.assertGreaterEqual(self.josh.stats['reading'], 0)
        self.assertGreaterEqual(self.josh.stats['completed'], 53)
        self.assertGreaterEqual(self.josh.stats['on_hold'], 0)
        self.assertGreaterEqual(self.josh.stats['dropped'], 0)
        self.assertGreaterEqual(self.josh.stats['plan_to_read'], 0)
        self.assertGreaterEqual(float(self.josh.stats['days_spent']), 25.41)

        self.assertIsInstance(self.threger.stats, dict)
        self.assertGreater(len(self.threger.stats), 0)
        self.assertEqual(self.threger.stats['reading'], 0)
        self.assertEqual(self.threger.stats['completed'], 0)
        self.assertEqual(self.threger.stats['on_hold'], 0)
        self.assertEqual(self.threger.stats['dropped'], 0)
        self.assertEqual(self.threger.stats['plan_to_read'], 0)
        self.assertEqual(float(self.threger.stats['days_spent']), 0.00)

    def testSection(self):
        self.assertIsInstance(self.shal.section('Completed'), dict)
        self.assertIn(self.tomoyo_after, self.shal.section('Completed'))
        self.assertIsInstance(self.pl.section('On-Hold'), dict)
        self.assertIn(self.amnesia, self.pl.section('On-Hold'))
        self.assertIsInstance(self.josh.section('Plan to Read'), dict)
        self.assertIn(self.jojo, self.josh.section('Plan to Read'))
        self.assertIsInstance(self.threger.section('Reading'), dict)
        self.assertEqual(len(self.threger.section('Reading')), 0)
