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

        self.shal = self.session.anime_list('shaldengeki')
        self.fz = self.session.anime(10087)
        self.trigun = self.session.anime(6)
        self.clannad = self.session.anime(2167)

        self.pl = self.session.anime_list('PaperLuigi')
        self.baccano = self.session.anime(2251)
        self.pokemon = self.session.anime(20159)
        self.dmc = self.session.anime(3702)

        self.mona = self.session.anime_list('monausicaa')
        self.zombie = self.session.anime(3354)
        self.lollipop = self.session.anime(1509)
        self.musume = self.session.anime(5246)
        self.ai_shite = self.session.anime(2221)

        self.threger = self.session.anime_list('threger')

    def testNoUsernameInvalidAnimeList(self):
        with self.assertRaises(TypeError):
            self.session.anime_list()

    def testNonexistentUsernameInvalidAnimeList(self):
        with self.assertRaises(myanimelist.media_list.InvalidMediaListError):
            self.session.anime_list('aspdoifpjsadoifjapodsijfp').load()

    def testUserValid(self):
        self.assertIsInstance(self.shal, myanimelist.anime_list.AnimeList)

    def testUsername(self):
        self.assertEqual(self.shal.username, 'shaldengeki')
        self.assertEqual(self.mona.username, 'monausicaa')

    def testType(self):
        self.assertEqual(self.shal.type, 'anime')

    def testList(self):
        self.assertIsInstance(self.shal.list, dict)
        self.assertEqual(len(self.shal), 146)

        self.assertIn(self.fz, self.shal)
        self.assertIn(self.clannad, self.shal)
        self.assertIn(self.trigun, self.shal)

        self.assertEqual(self.shal[self.fz]['status'], 'Watching')
        self.assertEqual(self.shal[self.clannad]['status'], 'Completed')
        self.assertEqual(self.shal[self.trigun]['status'], 'Plan to Watch')

        self.assertIsNone(self.shal[self.fz]['score'])
        self.assertEqual(self.shal[self.clannad]['score'], 9)
        self.assertIsNone(self.shal[self.trigun]['score'])

        self.assertEqual(self.shal[self.fz]['episodes_watched'], 6)
        self.assertEqual(self.shal[self.clannad]['episodes_watched'], 23)
        self.assertEqual(self.shal[self.trigun]['episodes_watched'], 6)

        self.assertIsNone(self.shal[self.fz]['started'])
        self.assertIsNone(self.shal[self.clannad]['started'])
        self.assertIsNone(self.shal[self.trigun]['started'])

        self.assertIsNone(self.shal[self.fz]['finished'])
        self.assertIsNone(self.shal[self.clannad]['finished'])
        self.assertIsNone(self.shal[self.trigun]['finished'])

        self.assertIsInstance(self.pl.list, dict)
        self.assertGreaterEqual(len(self.pl), 795)

        self.assertIn(self.baccano, self.pl)
        self.assertIn(self.pokemon, self.pl)
        self.assertIn(self.dmc, self.pl)

        self.assertEqual(self.pl[self.baccano]['status'], 'Completed')
        self.assertEqual(self.pl[self.pokemon]['status'], 'On-Hold')
        self.assertEqual(self.pl[self.dmc]['status'], 'Dropped')

        self.assertEqual(self.pl[self.baccano]['score'], 10)
        self.assertIsNone(self.pl[self.pokemon]['score'])
        self.assertEqual(self.pl[self.dmc]['score'], 2)

        self.assertEqual(self.pl[self.baccano]['episodes_watched'], 13)
        self.assertEqual(self.pl[self.pokemon]['episodes_watched'], 2)
        self.assertEqual(self.pl[self.dmc]['episodes_watched'], 1)

        self.assertEqual(self.pl[self.baccano]['started'], datetime.date(year=2009, month=7, day=27))
        self.assertEqual(self.pl[self.pokemon]['started'], datetime.date(year=2013, month=10, day=5))
        self.assertEqual(self.pl[self.dmc]['started'], datetime.date(year=2010, month=9, day=27))

        self.assertEqual(self.pl[self.baccano]['finished'], datetime.date(year=2009, month=7, day=28))
        self.assertIsNone(self.pl[self.pokemon]['finished'])
        self.assertIsNone(self.pl[self.dmc]['finished'])

        self.assertIsInstance(self.mona.list, dict)
        self.assertGreaterEqual(len(self.mona), 1822)

        self.assertIn(self.zombie, self.mona)
        self.assertIn(self.lollipop, self.mona)
        self.assertIn(self.musume, self.mona)

        self.assertEqual(self.mona[self.zombie]['status'], 'Completed')
        self.assertEqual(self.mona[self.lollipop]['status'], 'On-Hold')
        self.assertEqual(self.mona[self.musume]['status'], 'Completed')
        self.assertEqual(self.mona[self.ai_shite]['status'], 'Plan to Watch')

        self.assertEqual(self.mona[self.zombie]['score'], 7)
        self.assertIsNone(self.mona[self.lollipop]['score'])
        self.assertEqual(self.mona[self.musume]['score'], 5)

        self.assertEqual(self.mona[self.zombie]['episodes_watched'], 2)
        self.assertEqual(self.mona[self.lollipop]['episodes_watched'], 12)
        self.assertGreater(self.mona[self.musume]['episodes_watched'], 0)

        self.assertIsNone(self.mona[self.zombie]['started'])
        self.assertEqual(self.mona[self.lollipop]['started'], datetime.date(year=2013, month=4, day=14))
        self.assertIsNone(self.mona[self.musume]['started'])

        self.assertIsNone(self.mona[self.zombie]['finished'])
        self.assertIsNone(self.mona[self.lollipop]['finished'])
        self.assertIsNone(self.mona[self.musume]['finished'])

        self.assertIsInstance(self.threger.list, dict)
        self.assertEqual(len(self.threger), 0)

    def testStats(self):
        self.assertIsInstance(self.shal.stats, dict)
        self.assertGreater(len(self.shal.stats), 0)
        self.assertEqual(self.shal.stats['watching'], 10)
        self.assertEqual(self.shal.stats['completed'], 102)
        self.assertEqual(self.shal.stats['on_hold'], 1)
        self.assertEqual(self.shal.stats['dropped'], 5)
        self.assertEqual(self.shal.stats['plan_to_watch'], 28)
        self.assertGreaterEqual(float(self.shal.stats['days_spent']), 38.88)

        self.assertIsInstance(self.pl.stats, dict)
        self.assertGreater(len(self.pl.stats), 0)
        self.assertGreaterEqual(self.pl.stats['watching'], 0)
        self.assertGreaterEqual(self.pl.stats['completed'], 355)
        self.assertGreaterEqual(self.pl.stats['on_hold'], 0)
        self.assertGreaterEqual(self.pl.stats['dropped'], 385)
        self.assertGreaterEqual(self.pl.stats['plan_to_watch'], 0)
        self.assertGreaterEqual(float(self.pl.stats['days_spent']), 125.91)

        self.assertIsInstance(self.mona.stats, dict)
        self.assertGreater(len(self.mona.stats), 0)
        self.assertGreaterEqual(self.mona.stats['watching'], 0)
        self.assertGreaterEqual(self.mona.stats['completed'], 1721)
        self.assertGreaterEqual(self.mona.stats['on_hold'], 0)
        self.assertGreaterEqual(self.mona.stats['dropped'], 0)
        self.assertGreaterEqual(self.mona.stats['plan_to_watch'], 0)
        self.assertGreaterEqual(float(self.mona.stats['days_spent']), 470.30)

        self.assertIsInstance(self.threger.stats, dict)
        self.assertGreaterEqual(len(self.threger.stats), 0)
        self.assertEqual(self.threger.stats['watching'], 0)
        self.assertEqual(self.threger.stats['completed'], 0)
        self.assertEqual(self.threger.stats['on_hold'], 0)
        self.assertEqual(self.threger.stats['dropped'], 0)
        self.assertEqual(self.threger.stats['plan_to_watch'], 0)
        self.assertEqual(float(self.threger.stats['days_spent']), 0.00)

    def testSection(self):
        # shal
        self.assertIsInstance(self.shal.section('Watching'), dict)
        self.assertIn(self.fz, self.shal.section('Watching'))
        self.assertIsInstance(self.pl.section('Completed'), dict)
        self.assertIn(self.baccano, self.pl.section('Completed'))
        # mona
        self.assertIsInstance(self.mona.section('Plan to Watch'), dict)
        self.assertIn(self.musume, self.mona.section('Completed'))
        self.assertIn(self.ai_shite, self.mona.section('Plan to Watch'))
        # threger
        self.assertIsInstance(self.threger.section('Watching'), dict)
        self.assertEqual(len(self.threger.section('Watching')), 0)
