#!/usr/bin/python
# -*- coding: utf-8 -*-
from unittest import TestCase
import datetime

import myanimelist.session
import myanimelist.media_list
import myanimelist.anime_list


class testAnimeListClass(TestCase):
    @classmethod
    def setUpClass(self):
        self.session = myanimelist.session.Session()

        self.shal = self.session.anime_list(u'shaldengeki')
        self.fz = self.session.anime(10087)
        self.trigun = self.session.anime(6)
        self.clannad = self.session.anime(2167)

        self.pl = self.session.anime_list(u'PaperLuigi')
        self.baccano = self.session.anime(2251)
        self.pokemon = self.session.anime(20159)
        self.dmc = self.session.anime(3702)

        self.mona = self.session.anime_list(u'monausicaa')
        self.zombie = self.session.anime(3354)
        self.lollipop = self.session.anime(1509)
        self.musume = self.session.anime(5246)
        self.ai_shite = self.session.anime(2221)

        self.threger = self.session.anime_list(u'threger')

    def testNoUsernameInvalidAnimeList(self):
        with self.assertRaises(TypeError):
            self.session.anime_list()

    def testNonexistentUsernameInvalidAnimeList(self):
        with self.assertRaises(myanimelist.media_list.InvalidMediaListError):
            self.session.anime_list(u'aspdoifpjsadoifjapodsijfp').load()

    def testUserValid(self):
        self.assertIsInstance(self.shal, myanimelist.anime_list.AnimeList)

    def testUsername(self):
        self.assertEqual(self.shal.username, u'shaldengeki')
        self.assertEqual(self.mona.username, u'monausicaa')

    def testType(self):
        self.assertEqual(self.shal.type, u'anime')

    def testList(self):
        self.assertIsInstance(self.shal.list, dict)
        self.assertEqual(len(self.shal), 146)

        self.assertIn(self.fz, self.shal)
        self.assertIn(self.clannad, self.shal)
        self.assertIn(self.trigun, self.shal)

        self.assertEqual(self.shal[self.fz][u'status'], u'Watching')
        self.assertEqual(self.shal[self.clannad][u'status'], u'Completed')
        self.assertEqual(self.shal[self.trigun][u'status'], u'Plan to Watch')

        self.assertIsNone(self.shal[self.fz][u'score'])
        self.assertEqual(self.shal[self.clannad][u'score'], 9)
        self.assertIsNone(self.shal[self.trigun][u'score'])

        self.assertEqual(self.shal[self.fz][u'episodes_watched'], 6)
        self.assertEqual(self.shal[self.clannad][u'episodes_watched'], 23)
        self.assertEqual(self.shal[self.trigun][u'episodes_watched'], 6)

        self.assertIsNone(self.shal[self.fz][u'started'])
        self.assertIsNone(self.shal[self.clannad][u'started'])
        self.assertIsNone(self.shal[self.trigun][u'started'])

        self.assertIsNone(self.shal[self.fz][u'finished'])
        self.assertIsNone(self.shal[self.clannad][u'finished'])
        self.assertIsNone(self.shal[self.trigun][u'finished'])

        self.assertIsInstance(self.pl.list, dict)
        self.assertGreaterEqual(len(self.pl), 795)

        self.assertIn(self.baccano, self.pl)
        self.assertIn(self.pokemon, self.pl)
        self.assertIn(self.dmc, self.pl)

        self.assertEqual(self.pl[self.baccano][u'status'], u'Completed')
        self.assertEqual(self.pl[self.pokemon][u'status'], u'On-Hold')
        self.assertEqual(self.pl[self.dmc][u'status'], u'Dropped')

        self.assertEqual(self.pl[self.baccano][u'score'], 10)
        self.assertIsNone(self.pl[self.pokemon][u'score'])
        self.assertEqual(self.pl[self.dmc][u'score'], 2)

        self.assertEqual(self.pl[self.baccano][u'episodes_watched'], 13)
        self.assertEqual(self.pl[self.pokemon][u'episodes_watched'], 2)
        self.assertEqual(self.pl[self.dmc][u'episodes_watched'], 1)

        self.assertEqual(self.pl[self.baccano][u'started'], datetime.date(year=2009, month=7, day=27))
        self.assertEqual(self.pl[self.pokemon][u'started'], datetime.date(year=2013, month=10, day=5))
        self.assertEqual(self.pl[self.dmc][u'started'], datetime.date(year=2010, month=9, day=27))

        self.assertEqual(self.pl[self.baccano][u'finished'], datetime.date(year=2009, month=7, day=28))
        self.assertIsNone(self.pl[self.pokemon][u'finished'])
        self.assertIsNone(self.pl[self.dmc][u'finished'])

        self.assertIsInstance(self.mona.list, dict)
        self.assertGreaterEqual(len(self.mona), 1822)

        self.assertIn(self.zombie, self.mona)
        self.assertIn(self.lollipop, self.mona)
        self.assertIn(self.musume, self.mona)

        self.assertEqual(self.mona[self.zombie][u'status'], u'Completed')
        self.assertEqual(self.mona[self.lollipop][u'status'], u'On-Hold')
        self.assertEqual(self.mona[self.musume][u'status'], u'Completed')
        self.assertEqual(self.mona[self.ai_shite][u'status'], u'Plan to Watch')

        self.assertEqual(self.mona[self.zombie][u'score'], 7)
        self.assertIsNone(self.mona[self.lollipop][u'score'])
        self.assertIsNone(self.mona[self.musume][u'score'])

        self.assertEqual(self.mona[self.zombie][u'episodes_watched'], 2)
        self.assertEqual(self.mona[self.lollipop][u'episodes_watched'], 12)
        self.assertEqual(self.mona[self.musume][u'episodes_watched'], 0)

        self.assertIsNone(self.mona[self.zombie][u'started'])
        self.assertEqual(self.mona[self.lollipop][u'started'], datetime.date(year=2013, month=4, day=14))
        self.assertIsNone(self.mona[self.musume][u'started'])

        self.assertIsNone(self.mona[self.zombie][u'finished'])
        self.assertIsNone(self.mona[self.lollipop][u'finished'])
        self.assertIsNone(self.mona[self.musume][u'finished'])

        self.assertIsInstance(self.threger.list, dict)
        self.assertEqual(len(self.threger), 0)

    def testStats(self):
        self.assertIsInstance(self.shal.stats, dict)
        self.assertGreater(len(self.shal.stats), 0)
        self.assertEqual(self.shal.stats[u'watching'], 10)
        self.assertEqual(self.shal.stats[u'completed'], 102)
        self.assertEqual(self.shal.stats[u'on_hold'], 1)
        self.assertEqual(self.shal.stats[u'dropped'], 5)
        self.assertEqual(self.shal.stats[u'plan_to_watch'], 28)
        self.assertGreaterEqual(float(self.shal.stats[u'days_spent']), 38.88)

        self.assertIsInstance(self.pl.stats, dict)
        self.assertGreater(len(self.pl.stats), 0)
        self.assertGreaterEqual(self.pl.stats[u'watching'], 0)
        self.assertGreaterEqual(self.pl.stats[u'completed'], 355)
        self.assertGreaterEqual(self.pl.stats[u'on_hold'], 0)
        self.assertGreaterEqual(self.pl.stats[u'dropped'], 385)
        self.assertGreaterEqual(self.pl.stats[u'plan_to_watch'], 0)
        self.assertGreaterEqual(float(self.pl.stats[u'days_spent']), 125.91)

        self.assertIsInstance(self.mona.stats, dict)
        self.assertGreater(len(self.mona.stats), 0)
        self.assertGreaterEqual(self.mona.stats[u'watching'], 0)
        self.assertGreaterEqual(self.mona.stats[u'completed'], 1721)
        self.assertGreaterEqual(self.mona.stats[u'on_hold'], 0)
        self.assertGreaterEqual(self.mona.stats[u'dropped'], 0)
        self.assertGreaterEqual(self.mona.stats[u'plan_to_watch'], 0)
        self.assertGreaterEqual(float(self.mona.stats[u'days_spent']), 470.30)

        self.assertIsInstance(self.threger.stats, dict)
        self.assertGreaterEqual(len(self.threger.stats), 0)
        self.assertEqual(self.threger.stats[u'watching'], 0)
        self.assertEqual(self.threger.stats[u'completed'], 0)
        self.assertEqual(self.threger.stats[u'on_hold'], 0)
        self.assertEqual(self.threger.stats[u'dropped'], 0)
        self.assertEqual(self.threger.stats[u'plan_to_watch'], 0)
        self.assertEqual(float(self.threger.stats[u'days_spent']), 0.00)

    def testSection(self):
        # shal
        self.assertIsInstance(self.shal.section(u'Watching'), dict)
        self.assertIn(self.fz, self.shal.section(u'Watching'))
        self.assertIsInstance(self.pl.section(u'Completed'), dict)
        self.assertIn(self.baccano, self.pl.section(u'Completed'))
        # mona
        self.assertIsInstance(self.mona.section(u'Plan to Watch'), dict)
        self.assertIn(self.musume, self.mona.section(u'Completed'))
        self.assertIn(self.ai_shite, self.mona.section(u'Plan to Watch'))
        # threger
        self.assertIsInstance(self.threger.section(u'Watching'), dict)
        self.assertEqual(len(self.threger.section(u'Watching')), 0)
