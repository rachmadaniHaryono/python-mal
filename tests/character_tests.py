#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase

import myanimelist.session
import myanimelist.character
import myanimelist.user


try:
    unicode
    IS_PYTHON3 = False
except NameError:
    unicode = str
    IS_PYTHON3 = True

class testCharacterClass(TestCase):
    @classmethod
    def setUpClass(self):
        self.session = myanimelist.session.Session()
        self.spike = self.session.character(1)
        self.ed = self.session.character(11)
        self.maria = self.session.character(112693)
        self.invalid_character = self.session.character(457384754)
        self.suguru = self.session.character(88597)

    def testNoIDInvalidCharacter(self):
        with self.assertRaises(TypeError):
            self.session.character()

    def testNegativeInvalidCharacter(self):
        with self.assertRaises(myanimelist.character.InvalidCharacterError):
            self.session.character(-1)

    def testFloatInvalidCharacter(self):
        with self.assertRaises(myanimelist.character.InvalidCharacterError):
            self.session.character(1.5)

    def testNonExistentCharacter(self):
        with self.assertRaises(myanimelist.character.InvalidCharacterError):
            self.invalid_character.load()

    def testCharacterValid(self):
        self.assertIsInstance(self.spike, myanimelist.character.Character)
        self.assertIsInstance(self.maria, myanimelist.character.Character)

    def testName(self):
        self.assertEqual(self.spike.name, 'Spike Spiegel')
        self.assertEqual(self.ed.name, 'Edward Elric')
        self.assertEqual(self.maria.name, 'Maria')

    def testFullName(self):
        self.assertEqual(self.spike.full_name, 'Spike  Spiegel')
        self.assertEqual(self.ed.full_name,
                         'Edward "Ed, Fullmetal Alchemist, Hagane no shounen, Chibi, Pipsqueak" Elric')
        self.assertEqual(self.maria.full_name, 'Maria')

    def testJapaneseName(self):
        if IS_PYTHON3:
            self.assertEqual(self.spike.name_jpn, 'スパイク・スピーゲル')
            self.assertEqual(self.ed.name_jpn, 'エドワード・エルリック')
            self.assertEqual(self.maria.name_jpn, 'マリア')
        else:
            self.assertEqual(self.spike.name_jpn, u'スパイク・スピーゲル')
            self.assertEqual(self.ed.name_jpn, u'エドワード・エルリック')
            self.assertEqual(self.maria.name_jpn, u'マリア')
    def testDescription(self):
        self.assertIsInstance(self.spike.description, str)
        self.assertGreater(len(self.spike.description), 0)
        self.assertIsInstance(self.ed.description, str)
        self.assertGreater(len(self.ed.description), 0)
        self.assertIsInstance(self.maria.description, str)
        self.assertGreater(len(self.maria.description), 0)

    def testPicture(self):
        self.assertIsInstance(self.spike.picture, unicode)
        self.assertGreater(len(self.spike.picture), 0)
        self.assertIsInstance(self.ed.picture, unicode)
        self.assertGreater(len(self.ed.picture), 0)
        self.assertIsInstance(self.maria.picture, unicode)
        self.assertGreater(len(self.maria.picture), 0)

    def testPictures(self):
        self.assertIsInstance(self.spike.pictures, list)
        self.assertGreater(len(self.spike.pictures), 0)
        for p in self.spike.pictures:
            self.assertIsInstance(p, unicode)
            self.assertTrue(p.startswith('http://'))
        self.assertIsInstance(self.ed.pictures, list)
        self.assertGreater(len(self.ed.pictures), 0)
        for p in self.spike.pictures:
            self.assertIsInstance(p, unicode)
            self.assertTrue(p.startswith('http://'))
        self.assertIsInstance(self.maria.pictures, list)

    def testAnimeography(self):
        self.assertIsInstance(self.spike.animeography, dict)
        self.assertGreater(len(self.spike.animeography), 0)
        self.assertIn(self.session.anime(1), self.spike.animeography)
        self.assertIsInstance(self.ed.animeography, dict)
        self.assertGreater(len(self.ed.animeography), 0)
        self.assertIn(self.session.anime(5114), self.ed.animeography)
        self.assertIsInstance(self.maria.animeography, dict)
        self.assertGreater(len(self.maria.animeography), 0)
        self.assertIn(self.session.anime(26441), self.maria.animeography)

    def testMangaography(self):
        self.assertIsInstance(self.spike.mangaography, dict)
        self.assertGreater(len(self.spike.mangaography), 0)
        self.assertIn(self.session.manga(173), self.spike.mangaography)
        self.assertIsInstance(self.ed.mangaography, dict)
        self.assertGreater(len(self.ed.mangaography), 0)
        self.assertIn(self.session.manga(4658), self.ed.mangaography)
        self.assertIsInstance(self.maria.mangaography, dict)
        self.assertGreater(len(self.maria.mangaography), 0)
        self.assertIn(self.session.manga(12336), self.maria.mangaography)

    def testNumFavorites(self):
        self.assertIsInstance(self.spike.num_favorites, int)
        self.assertGreater(self.spike.num_favorites, 12000)
        self.assertIsInstance(self.ed.num_favorites, int)
        self.assertGreater(self.ed.num_favorites, 19000)
        self.assertIsInstance(self.maria.num_favorites, int)

    def testFavorites(self):
        pass
        '''
        self.assertIsInstance(self.spike.favorites, list)
        self.assertGreater(len(self.spike.favorites), 12000)
        for u in self.spike.favorites:
            self.assertIsInstance(u, myanimelist.user.User)
        self.assertIsInstance(self.ed.favorites, list)
        self.assertGreater(len(self.ed.favorites), 19000)
        for u in self.ed.favorites:
            self.assertIsInstance(u, myanimelist.user.User)
        self.assertIsInstance(self.maria.favorites, list)
        '''

    def testClubs(self):
        self.assertIsInstance(self.spike.clubs, list)
        self.assertGreater(len(self.spike.clubs), 0)
        for u in self.spike.clubs:
            self.assertIsInstance(u, myanimelist.club.Club)
        self.assertIsInstance(self.ed.clubs, list)
        self.assertGreater(len(self.ed.clubs), 0)
        for u in self.spike.clubs:
            self.assertIsInstance(u, myanimelist.club.Club)
        self.assertIsInstance(self.maria.clubs, list)

    def testNoVoiceActors(self):
        self.assertIsNone(self.suguru.voice_actors)
