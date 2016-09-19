#!/usr/bin/python
# -*- coding: utf-8 -*-
"""module to test manga."""

from unittest import TestCase
import datetime

from six import string_types

import myanimelist.session
import myanimelist.manga

try:
    unicode
    IS_PYTHON3 = False
except NameError:
    unicode = str
    IS_PYTHON3 = True


class TestMangaClass(TestCase):
    """test manga class."""

    @classmethod
    def setUpClass(cls):
        """set up class."""
        cls.session = myanimelist.session.Session()

        cls.monster = cls.session.manga(1)
        cls.mystery = cls.session.genre(7)
        cls.mystery_tag = cls.session.tag(u'mystery')
        cls.urasawa = cls.session.person(1867)
        cls.original = cls.session.publication(1)
        cls.heinemann = cls.session.character(6123)
        cls.monster_side_story = cls.session.manga(10968)

        cls.holic = cls.session.manga(10)
        cls.supernatural = cls.session.genre(37)
        cls.supernatural_tag = cls.session.tag(u'supernatural')
        cls.clamp = cls.session.person(1877)
        cls.bessatsu = cls.session.publication(450)
        cls.doumeki = cls.session.character(567)
        cls.holic_sequel = cls.session.manga(46010)

        cls.naruto = cls.session.manga(11)
        cls.shounen = cls.session.genre(27)
        cls.action_tag = cls.session.tag(u'action')
        cls.kishimoto = cls.session.person(1879)
        cls.shonen_jump_weekly = cls.session.publication(83)
        cls.ebizou = cls.session.character(31825)

        cls.tomoyo_after = cls.session.manga(3941)
        cls.drama = cls.session.genre(8)
        cls.romance_tag = cls.session.tag(u'romance')
        cls.sumiyoshi = cls.session.person(3830)
        cls.dragon_age = cls.session.publication(98)
        cls.kanako = cls.session.character(21227)

        cls.judos = cls.session.manga(79819)
        cls.action = cls.session.genre(1)
        cls.kondou = cls.session.person(18765)

        cls.invalid_manga = cls.session.manga(457384754)
        cls.latest_manga = myanimelist.manga.Manga.newest(cls.session)

    def test_no_id_invalid_manga(self):
        """test no id and invalid manga."""
        with self.assertRaises(TypeError):
            self.session.manga()

    def test_no_session_invalid_latest_manga(self):
        """test no session."""
        with self.assertRaises(TypeError):
            myanimelist.manga.Manga.newest()

    def test_negative_invalid_manga(self):
        """test negative manga id."""
        with self.assertRaises(myanimelist.manga.InvalidMangaError):
            self.session.manga(-1)

    def test_float_invalid_manga(self):
        """test float invalid manga id."""
        with self.assertRaises(myanimelist.manga.InvalidMangaError):
            self.session.manga(1.5)

    def test_non_existent_manga(self):
        """test non existent manga."""
        with self.assertRaises(myanimelist.manga.MalformedMangaPageError):
            self.invalid_manga.load()

    def test_latest_manga(self):
        """test latest manga."""
        self.assertIsInstance(self.latest_manga, myanimelist.manga.Manga)
        self.assertGreater(self.latest_manga.id, 79818)

    def test_manga_valid(self):
        """test valid manga."""
        self.assertIsInstance(self.monster, myanimelist.manga.Manga)

    def test_title(self):
        """title."""
        self.assertEqual(self.monster.title, u'Monster')
        self.assertEqual(self.holic.title, u'xxxHOLiC')
        self.assertEqual(self.naruto.title, u'Naruto')
        self.assertEqual(self.tomoyo_after.title, u'Clannad: Tomoyo After')
        self.assertEqual(self.judos.title, u'Judos')

    def test_picture(self):
        """test picture."""
        self.assertIsInstance(self.holic.picture, string_types)
        self.assertIsInstance(self.naruto.picture, string_types)
        self.assertIsInstance(self.monster.picture, string_types)
        self.assertIsInstance(self.tomoyo_after.picture, string_types)
        self.assertIsInstance(self.judos.picture, string_types)

    def test_alternative_tit_greater(self):
        """test alternative_titles."""
        self.assertIn(u'Japanese', self.monster.alternative_titles)
        self.assertIsInstance(self.monster.alternative_titles[u'Japanese'], list)
        # http://myanimelist.net/manga/1/Monster
        # japanese alternative title for monster manga is 'MONSTER'
        self.assertIn(u'MONSTER', self.monster.alternative_titles[u'Japanese'])
        self.assertIn(u'Synonyms', self.holic.alternative_titles)
        self.assertIsInstance(self.holic.alternative_titles[u'Synonyms'], list)
        self.assertIn(u'xxxHolic Cage', self.holic.alternative_titles[u'Synonyms'])
        self.assertIn(u'Japanese', self.naruto.alternative_titles)
        self.assertIsInstance(self.naruto.alternative_titles[u'Japanese'], list)
        self.assertIn(u'NARUTO―ナルト―', self.naruto.alternative_titles[u'Japanese'])
        self.assertIn(u'English', self.tomoyo_after.alternative_titles)
        self.assertIsInstance(self.tomoyo_after.alternative_titles[u'English'], list)
        self.assertIn(
            u'Tomoyo After ~Dear Shining Memories~',
            self.tomoyo_after.alternative_titles[u'English']
        )
        self.assertIn(u'Synonyms', self.judos.alternative_titles)
        self.assertIsInstance(self.judos.alternative_titles[u'Synonyms'], list)
        self.assertIn(u'Juudouzu', self.judos.alternative_titles[u'Synonyms'])

    def test_types(self):
        """test type."""
        self.assertEqual(self.monster.type, u'Manga')
        self.assertEqual(self.tomoyo_after.type, u'Manga')
        self.assertEqual(self.judos.type, u'Manga')

    def test_volumes(self):
        """test volumes."""
        self.assertEqual(self.holic.volumes, 19)
        self.assertEqual(self.monster.volumes, 18)
        self.assertEqual(self.tomoyo_after.volumes, 1)
        self.assertEqual(self.naruto.volumes, 72)
        self.assertEqual(self.judos.volumes, 3)

    def test_chapters(self):
        """test chapters."""
        self.assertEqual(self.holic.chapters, 213)
        self.assertEqual(self.monster.chapters, 162)
        self.assertEqual(self.tomoyo_after.chapters, 4)
        self.assertEqual(self.naruto.chapters, 700)
        # update from 27-8-2015 judos is finished with 21 chapter
        self.assertEqual(self.judos.chapters, 21)

    def test_status(self):
        """test status."""
        self.assertEqual(self.holic.status, u'Finished')
        self.assertEqual(self.tomoyo_after.status, u'Finished')
        self.assertEqual(self.monster.status, u'Finished')
        self.assertEqual(self.naruto.status, u'Finished')

    def test_published(self):
        """test published."""
        self.assertEqual(self.holic.published, (datetime.date(month=2, day=24, year=2003),
                         datetime.date(month=2, day=9, year=2011)))
        self.assertEqual(self.monster.published, (datetime.date(month=12, day=5, year=1994),
                         datetime.date(month=12, day=20, year=2001)))
        self.assertEqual(self.naruto.published, (datetime.date(month=9, day=21, year=1999),
                         datetime.date(month=11, day=10, year=2014)))
        self.assertEqual(self.tomoyo_after.published, (datetime.date(month=4, day=20, year=2007),
                         datetime.date(month=10, day=20, year=2007)))

    def test_genres(self):
        """test genres."""
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

    def test_authors(self):
        """test authors."""
        self.assertIsInstance(self.holic.authors, dict)
        self.assertGreater(len(self.holic.authors), 0)
        self.assertIn(self.clamp, self.holic.authors)
        self.assertEqual(self.holic.authors[self.clamp], u'Story & Art')

        self.assertIsInstance(self.tomoyo_after.authors, dict)
        self.assertGreater(len(self.tomoyo_after.authors), 0)
        self.assertIn(self.sumiyoshi, self.tomoyo_after.authors)
        self.assertEqual(self.tomoyo_after.authors[self.sumiyoshi], u'Art')

        self.assertIsInstance(self.naruto.authors, dict)
        self.assertGreater(len(self.naruto.authors), 0)
        self.assertIn(self.kishimoto, self.naruto.authors)
        self.assertEqual(self.naruto.authors[self.kishimoto], u'Story & Art')

        self.assertIsInstance(self.monster.authors, dict)
        self.assertGreater(len(self.monster.authors), 0)
        self.assertIn(self.urasawa, self.monster.authors)
        self.assertEqual(self.monster.authors[self.urasawa], u'Story & Art')

        self.assertIsInstance(self.judos.authors, dict)
        self.assertGreater(len(self.judos.authors), 0)
        self.assertIn(self.kondou, self.judos.authors)
        self.assertEqual(self.judos.authors[self.kondou], 'Story & Art')

    def test_serialization(self):
        """test serialization."""
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

    def test_score(self):
        """test score."""
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

    def test_rank(self):
        """test rank."""
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

    def test_popularity(self):
        """test popularity."""
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

    def test_members(self):
        """test members."""
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

    def test_favorites(self):
        """test favorites."""
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

    def test_popular_tags(self):
        """test popular tags.
        
        .. deprecated:: 0.1.8
            Popular tags test is not available anymore.
        """
        pass

    def test_synopsis(self):
        """test synopsis."""
        self.assertIsInstance(self.holic.synopsis, string_types)
        self.assertGreater(len(self.holic.synopsis), 0)
        self.assertIn(u'Watanuki', self.holic.synopsis)

        self.assertIsInstance(self.monster.synopsis, string_types)
        self.assertGreater(len(self.monster.synopsis), 0)
        self.assertIn(u'Tenma', self.monster.synopsis)

        self.assertIsInstance(self.naruto.synopsis, string_types)
        self.assertGreater(len(self.naruto.synopsis), 0)
        self.assertIn(u'Hokage', self.naruto.synopsis)

        self.assertIsInstance(self.tomoyo_after.synopsis, string_types)
        self.assertGreater(len(self.tomoyo_after.synopsis), 0)
        self.assertIn(u'Clannad', self.tomoyo_after.synopsis)

        self.assertIsInstance(self.judos.synopsis, string_types)
        self.assertGreater(len(self.judos.synopsis), 0)
        self.assertIn(u'hardcore', self.judos.synopsis)

    def test_related(self):
        """test related."""
        self.assertIsInstance(self.holic.related, dict)
        self.assertIn('Sequel', self.holic.related)
        self.assertIn(self.holic_sequel, self.holic.related['Sequel'])
        self.assertIsInstance(self.monster.related, dict)
        self.assertIn('Side story', self.monster.related)
        self.assertIn(self.monster_side_story, self.monster.related['Side story'])

    def test_characters(self):
        """test characters."""
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
