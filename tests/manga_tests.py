#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase
import datetime

import myanimelist.session
import myanimelist.manga


class testMangaClass(TestCase):
    @classmethod
    def setUpClass(self):
        self.session = myanimelist.session.Session()

        self.monster = self.session.manga(1)
        self.mystery = self.session.genre(7)
        self.mystery_tag = self.session.tag('mystery')
        self.urasawa = self.session.person(1867)
        self.original = self.session.publication(1)
        self.heinemann = self.session.character(6123)
        self.monster_side_story = self.session.manga(10968)

        self.holic = self.session.manga(10)
        self.supernatural = self.session.genre(37)
        self.supernatural_tag = self.session.tag('supernatural')
        self.clamp = self.session.person(1877)
        self.bessatsu = self.session.publication(450)
        self.doumeki = self.session.character(567)
        self.holic_sequel = self.session.manga(46010)

        self.naruto = self.session.manga(11)
        self.shounen = self.session.genre(27)
        self.action_tag = self.session.tag('action')
        self.kishimoto = self.session.person(1879)
        self.shonen_jump_weekly = self.session.publication(83)
        self.ebizou = self.session.character(31825)

        self.tomoyo_after = self.session.manga(3941)
        self.drama = self.session.genre(8)
        self.romance_tag = self.session.tag('romance')
        self.sumiyoshi = self.session.person(3830)
        self.dragon_age = self.session.publication(98)
        self.kanako = self.session.character(21227)

        self.judos = self.session.manga(79819)
        self.action = self.session.genre(1)
        self.kondou = self.session.person(18765)

        self.invalid_manga = self.session.manga(457384754)
        self.latest_manga = myanimelist.manga.Manga.newest(self.session)

    def testNoIDInvalidManga(self):
        with self.assertRaises(TypeError):
            self.session.manga()

    def testNoSessionInvalidLatestManga(self):
        with self.assertRaises(TypeError):
            myanimelist.manga.Manga.newest()

    def testNegativeInvalidManga(self):
        with self.assertRaises(myanimelist.manga.InvalidMangaError):
            self.session.manga(-1)

    def testFloatInvalidManga(self):
        with self.assertRaises(myanimelist.manga.InvalidMangaError):
            self.session.manga(1.5)

    def testNonExistentManga(self):
        with self.assertRaises(myanimelist.manga.MalformedMangaPageError):
            self.invalid_manga.load()

    def testLatestManga(self):
        self.assertIsInstance(self.latest_manga, myanimelist.manga.Manga)
        self.assertGreater(self.latest_manga.id, 79818)

    def testMangaValid(self):
        self.assertIsInstance(self.monster, myanimelist.manga.Manga)

    def testTitle(self):
        self.assertEqual(self.monster.title, 'Monster')
        self.assertEqual(self.holic.title, 'xxxHOLiC')
        self.assertEqual(self.naruto.title, 'Naruto')
        self.assertEqual(self.tomoyo_after.title, 'Clannad: Tomoyo After')
        self.assertEqual(self.judos.title, 'Judos')

    def testPicture(self):
        self.assertIsInstance(self.holic.picture, str)
        self.assertIsInstance(self.naruto.picture, str)
        self.assertIsInstance(self.monster.picture, str)
        self.assertIsInstance(self.tomoyo_after.picture, str)
        self.assertIsInstance(self.judos.picture, str)

    def testAlternativeTitGreater(self):
        self.assertIn('Japanese', self.monster.alternative_titles)
        self.assertIsInstance(self.monster.alternative_titles['Japanese'], list)
        # http://myanimelist.net/manga/1/Monster
        # japanese alternative title for monster manga is 'MONSTER'
        self.assertIn('MONSTER', self.monster.alternative_titles['Japanese'])
        self.assertIn('Synonyms', self.holic.alternative_titles)
        self.assertIsInstance(self.holic.alternative_titles['Synonyms'], list)
        self.assertIn('xxxHolic Cage', self.holic.alternative_titles['Synonyms'])
        self.assertIn('Japanese', self.naruto.alternative_titles)
        self.assertIsInstance(self.naruto.alternative_titles['Japanese'], list)
        self.assertIn('NARUTO\u2015\u30ca\u30eb\u30c8\u2015',
                      self.naruto.alternative_titles['Japanese'])
        self.assertIn('English', self.tomoyo_after.alternative_titles)
        self.assertIsInstance(self.tomoyo_after.alternative_titles['English'], list)
        self.assertIn('Tomoyo After ~Dear Shining Memories~', self.tomoyo_after.alternative_titles['English'])
        self.assertIn('Synonyms', self.judos.alternative_titles)
        self.assertIsInstance(self.judos.alternative_titles['Synonyms'], list)
        self.assertIn('Juudouzu', self.judos.alternative_titles['Synonyms'])

    def testTypes(self):
        self.assertEqual(self.monster.type, 'Manga')
        self.assertEqual(self.tomoyo_after.type, 'Manga')
        self.assertEqual(self.judos.type, 'Manga')

    def testVolumes(self):
        self.assertEqual(self.holic.volumes, 19)
        self.assertEqual(self.monster.volumes, 18)
        self.assertEqual(self.tomoyo_after.volumes, 1)
        self.assertEqual(self.naruto.volumes, 72)
        self.assertEqual(self.judos.volumes, 3)

    def testChapters(self):
        self.assertEqual(self.holic.chapters, 213)
        self.assertEqual(self.monster.chapters, 162)
        self.assertEqual(self.tomoyo_after.chapters, 4)
        self.assertEqual(self.naruto.chapters, 700)
        # update from 27-8-2015 judos is finished with 21 chapter
        self.assertEqual(self.judos.chapters, 21)

    def testStatus(self):
        self.assertEqual(self.holic.status, 'Finished')
        self.assertEqual(self.tomoyo_after.status, 'Finished')
        self.assertEqual(self.monster.status, 'Finished')
        self.assertEqual(self.naruto.status, 'Finished')

    def testPublished(self):
        self.assertEqual(self.holic.published, (datetime.date(month=2, day=24, year=2003),
                         datetime.date(month=2, day=9, year=2011)))
        self.assertEqual(self.monster.published, (datetime.date(month=12, day=5, year=1994),
                         datetime.date(month=12, day=20, year=2001)))
        self.assertEqual(self.naruto.published, (datetime.date(month=9, day=21, year=1999),
                         datetime.date(month=11, day=10, year=2014)))
        self.assertEqual(self.tomoyo_after.published, (datetime.date(month=4, day=20, year=2007),
                         datetime.date(month=10, day=20, year=2007)))

    def testGenres(self):
        """test manga genres."""
        self.assertIsInstance(self.holic.genres, list)
        self.assertGreater(len(self.holic.genres), 0)
        self.assertIn(self.mystery, self.holic.genres)
        self.assertIn(self.supernatural, self.holic.genres)

        self.assertIsInstance(self.tomoyo_after.genres, list)
        self.assertGreater(len(self.tomoyo_after.genres), 0)
        self.assertIn(self.drama, self.tomoyo_after.genres)

        self.assertIsInstance(self.naruto.genres, list)
        self.assertGreater(len(self.naruto.genres), 0)
        self.assertIn(self.shounen, self.naruto.genres)

        self.assertIsInstance(self.monster.genres, list)
        self.assertGreater(len(self.monster.genres), 0)
        self.assertIn(self.mystery, self.monster.genres)

        self.assertIsInstance(self.judos.genres, list)
        self.assertGreater(len(self.judos.genres), 0)
        self.assertIn(self.shounen, self.judos.genres)
        self.assertIn(self.action, self.judos.genres)

    def testAuthors(self):
        """test manga authors."""
        self.assertIsInstance(self.holic.authors, dict)
        self.assertGreater(len(self.holic.authors), 0)
        self.assertIn(self.clamp, self.holic.authors)
        self.assertEqual(self.holic.authors[self.clamp], 'Story & Art')

        self.assertIsInstance(self.tomoyo_after.authors, dict)
        self.assertGreater(len(self.tomoyo_after.authors), 0)
        self.assertIn(self.sumiyoshi, self.tomoyo_after.authors)
        self.assertEqual(self.tomoyo_after.authors[self.sumiyoshi], 'Art')

        self.assertIsInstance(self.naruto.authors, dict)
        self.assertGreater(len(self.naruto.authors), 0)
        self.assertIn(self.kishimoto, self.naruto.authors)
        self.assertEqual(self.naruto.authors[self.kishimoto], 'Story & Art')

        self.assertIsInstance(self.monster.authors, dict)
        self.assertGreater(len(self.monster.authors), 0)
        self.assertIn(self.urasawa, self.monster.authors)
        self.assertEqual(self.monster.authors[self.urasawa], 'Story & Art')

        self.assertIsInstance(self.judos.authors, dict)
        self.assertGreater(len(self.judos.authors), 0)
        self.assertIn(self.kondou, self.judos.authors)
        self.assertEqual(self.judos.authors[self.kondou], 'Story & Art')

    def testSerialization(self):
        self.assertIsInstance(self.holic.serialization, myanimelist.publication.Publication)
        self.assertEqual(self.bessatsu, self.holic.serialization)
        self.assertIsInstance(self.tomoyo_after.serialization, myanimelist.publication.Publication)
        self.assertEqual(self.dragon_age, self.tomoyo_after.serialization)
        self.assertIsInstance(self.naruto.serialization, myanimelist.publication.Publication)
        self.assertEqual(self.shonen_jump_weekly, self.naruto.serialization)
        self.assertIsInstance(self.monster.serialization, myanimelist.publication.Publication)
        self.assertEqual(self.original, self.monster.serialization)
        self.assertIsInstance(self.judos.serialization, myanimelist.publication.Publication)
        self.assertEqual(self.shonen_jump_weekly, self.judos.serialization)

    def testScore(self):
        self.assertIsInstance(self.holic.score, tuple)
        self.assertGreater(self.holic.score[0], 0)
        self.assertLess(self.holic.score[0], 10)
        self.assertIsInstance(self.holic.score[1], int)
        self.assertGreater(self.holic.score[1], 0)

        self.assertIsInstance(self.monster.score, tuple)
        self.assertGreater(self.monster.score[0], 0)
        self.assertLess(self.monster.score[0], 10)
        self.assertIsInstance(self.monster.score[1], int)
        self.assertGreater(self.monster.score[1], 0)

        self.assertIsInstance(self.naruto.score, tuple)
        self.assertGreater(self.naruto.score[0], 0)
        self.assertLess(self.naruto.score[0], 10)
        self.assertIsInstance(self.naruto.score[1], int)
        self.assertGreater(self.naruto.score[1], 0)

        self.assertIsInstance(self.tomoyo_after.score, tuple)
        self.assertGreater(self.tomoyo_after.score[0], 0)
        self.assertLess(self.tomoyo_after.score[0], 10)
        self.assertIsInstance(self.tomoyo_after.score[1], int)
        self.assertGreater(self.tomoyo_after.score[1], 0)

        self.assertGreater(self.judos.score[0], 0)
        self.assertLess(self.judos.score[0], 10)
        self.assertIsInstance(self.judos.score[1], int)
        self.assertGreater(self.judos.score[1], 0)

    def testRank(self):
        self.assertIsInstance(self.holic.rank, int)
        self.assertGreater(self.holic.rank, 0)
        self.assertIsInstance(self.monster.rank, int)
        self.assertGreater(self.monster.rank, 0)
        self.assertIsInstance(self.naruto.rank, int)
        self.assertGreater(self.naruto.rank, 0)
        self.assertIsInstance(self.tomoyo_after.rank, int)
        self.assertGreater(self.tomoyo_after.rank, 0)
        self.assertIsInstance(self.judos.rank, int)
        self.assertGreater(self.judos.rank, 0)

    def testPopularity(self):
        self.assertIsInstance(self.holic.popularity, int)
        self.assertGreater(self.holic.popularity, 0)
        self.assertIsInstance(self.monster.popularity, int)
        self.assertGreater(self.monster.popularity, 0)
        self.assertIsInstance(self.naruto.popularity, int)
        self.assertGreater(self.naruto.popularity, 0)
        self.assertIsInstance(self.tomoyo_after.popularity, int)
        self.assertGreater(self.tomoyo_after.popularity, 0)
        self.assertIsInstance(self.judos.popularity, int)
        self.assertGreater(self.judos.popularity, 0)

    def testMembers(self):
        self.assertIsInstance(self.holic.members, int)
        self.assertGreater(self.holic.members, 0)
        self.assertIsInstance(self.monster.members, int)
        self.assertGreater(self.monster.members, 0)
        self.assertIsInstance(self.naruto.members, int)
        self.assertGreater(self.naruto.members, 0)
        self.assertIsInstance(self.tomoyo_after.members, int)
        self.assertGreater(self.tomoyo_after.members, 0)
        self.assertIsInstance(self.judos.members, int)
        self.assertGreater(self.judos.members, 0)

    def testFavorites(self):
        self.assertIsInstance(self.holic.favorites, int)
        self.assertGreater(self.holic.favorites, 0)
        self.assertIsInstance(self.monster.favorites, int)
        self.assertGreater(self.monster.favorites, 0)
        self.assertIsInstance(self.naruto.favorites, int)
        self.assertGreater(self.naruto.favorites, 0)
        self.assertIsInstance(self.tomoyo_after.favorites, int)
        self.assertGreater(self.tomoyo_after.favorites, 0)
        self.assertIsInstance(self.judos.favorites, int)
        self.assertGreaterEqual(self.judos.favorites, 0)

    def testPopularTags(self):
        """test manga popular tags."""
        self.assertIsInstance(self.holic.popular_tags, dict)
        self.assertGreater(len(self.holic.popular_tags), 0)
        self.assertIn(self.supernatural_tag, self.holic.popular_tags)
        # no ranking of tag found after website update.
        # self.assertGreater(self.holic.popular_tags[self.supernatural_tag], 269)

        self.assertIsInstance(self.tomoyo_after.popular_tags, dict)
        self.assertGreater(len(self.tomoyo_after.popular_tags), 0)
        self.assertIn(self.romance_tag, self.tomoyo_after.popular_tags)

        self.assertIsInstance(self.naruto.popular_tags, dict)
        self.assertGreater(len(self.naruto.popular_tags), 0)
        self.assertIn(self.action_tag, self.naruto.popular_tags)

        self.assertIsInstance(self.monster.popular_tags, dict)
        self.assertGreater(len(self.monster.popular_tags), 0)
        self.assertIn(self.mystery_tag, self.monster.popular_tags)

        self.assertIsInstance(self.judos.popular_tags, dict)
        self.assertGreater(len(self.judos.popular_tags), 0)

    def testSynopsis(self):
        """test manga synopsis."""
        self.assertIsInstance(self.holic.synopsis, str)
        self.assertGreater(len(self.holic.synopsis), 0)
        self.assertIn('Watanuki', self.holic.synopsis)

        self.assertIsInstance(self.monster.synopsis, str)
        self.assertGreater(len(self.monster.synopsis), 0)
        self.assertIn('Tenma', self.monster.synopsis)

        self.assertIsInstance(self.naruto.synopsis, str)
        self.assertGreater(len(self.naruto.synopsis), 0)
        self.assertIn('Hokage', self.naruto.synopsis)

        self.assertIsInstance(self.tomoyo_after.synopsis, str)
        self.assertGreater(len(self.tomoyo_after.synopsis), 0)
        self.assertIn('Clannad', self.tomoyo_after.synopsis)

        self.assertIsInstance(self.judos.synopsis, str)
        self.assertGreater(len(self.judos.synopsis), 0)
        self.assertIn('hardcore', self.judos.synopsis)

    def testRelated(self):
        self.assertIsInstance(self.holic.related, dict)
        self.assertIn('Sequel', self.holic.related)
        self.assertIn(self.holic_sequel, self.holic.related['Sequel'])
        self.assertIsInstance(self.monster.related, dict)
        self.assertIn('Side story', self.monster.related)
        self.assertIn(self.monster_side_story, self.monster.related['Side story'])

    def testCharacters(self):
        """test manga characters."""
        self.assertIsInstance(self.holic.characters, dict)
        self.assertGreater(len(self.holic.characters), 0)
        self.assertIn(self.doumeki, self.holic.characters)
        self.assertEqual(self.holic.characters[self.doumeki]['role'], 'Main')

        self.assertIsInstance(self.monster.characters, dict)
        self.assertGreater(len(self.monster.characters), 0)
        self.assertIn(self.heinemann, self.monster.characters)
        self.assertEqual(self.monster.characters[self.heinemann]['role'], 'Main')

        self.assertIsInstance(self.naruto.characters, dict)
        self.assertGreater(len(self.naruto.characters), 0)
        self.assertIn(self.ebizou, self.naruto.characters)
        self.assertEqual(self.naruto.characters[self.ebizou]['role'], 'Supporting')

        self.assertIsInstance(self.tomoyo_after.characters, dict)
        self.assertGreater(len(self.tomoyo_after.characters), 0)
        self.assertIn(self.kanako, self.tomoyo_after.characters)
        self.assertEqual(self.tomoyo_after.characters[self.kanako]['role'], 'Supporting')
