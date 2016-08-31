#!/usr/bin/python
# -*- coding: utf-8 -*-
"""test module for anime parser."""
from unittest import TestCase
import datetime

import myanimelist.session
import myanimelist.anime


class TestAnimeClass(TestCase):
    """test anime parser."""

    @classmethod
    def setUpClass(cls):
        """set up class."""
        cls.session = myanimelist.session.Session()
        cls.bebop = cls.session.anime(1)
        cls.sunrise = cls.session.producer(14)
        cls.bandai_visual = cls.session.producer(23)
        cls.action = cls.session.genre(1)
        cls.hex = cls.session.character(94717)
        cls.hex_va = cls.session.person(5766)
        cls.bebop_side_story = cls.session.anime(5)
        cls.space_tag = cls.session.tag('space')

        cls.spicy_wolf = cls.session.anime(2966)
        cls.kadokawa = cls.session.producer(352)
        cls.romance = cls.session.genre(22)
        cls.holo = cls.session.character(7373)
        cls.holo_va = cls.session.person(70)
        cls.spicy_wolf_sequel = cls.session.anime(6007)
        cls.adventure_tag = cls.session.tag(u'adventure')

        cls.space_dandy = cls.session.anime(20057)
        cls.funi = cls.session.producer(102)
        cls.scifi = cls.session.genre(24)
        cls.toaster = cls.session.character(110427)
        cls.toaster_va = cls.session.person(611)

        cls.totoro = cls.session.anime(523)
        cls.gkids = cls.session.producer(783)
        cls.studio_fantasia = cls.session.producer(24)
        cls.supernatural = cls.session.genre(37)
        cls.satsuki = cls.session.character(267)
        cls.satsuki_va = cls.session.person(1104)

        cls.prisma = cls.session.anime(18851)
        cls.silver_link = cls.session.producer(300)
        cls.fantasy = cls.session.genre(10)
        cls.ilya = cls.session.character(503)
        cls.ilya_va = cls.session.person(117)

        cls.invalid_anime = cls.session.anime(457384754)
        cls.latest_anime = myanimelist.anime.Anime.newest(cls.session)

        cls.non_tagged_anime = cls.session.anime(10448)
        # this anime is not non_tagged but only have one tag(drama)

        # test character without va
        cls.non_non_biyori = cls.session.anime(17549)
        cls.suguru = cls.session.character(88597)

    def test_no_id_invalid_anime(self):
        """test for invalid in input."""
        with self.assertRaises(TypeError):
            self.session.anime()

    def test_no_session_invalid_latestanime(self):
        """test for when session is invalid."""
        with self.assertRaises(TypeError):
            myanimelist.anime.Anime.newest()

    def test_negative_invalid_anime(self):
        """test for negative invalid anime."""
        with self.assertRaises(myanimelist.anime.InvalidAnimeError):
            self.session.anime(-1)

    def test_float_invalid_anime(self):
        """test for float input."""
        with self.assertRaises(myanimelist.anime.InvalidAnimeError):
            self.session.anime(1.5)

    def test_non_existent_anime(self):
        """test for non existence anime."""
        with self.assertRaises(myanimelist.anime.MalformedAnimePageError):
            self.invalid_anime.load()

    def test_latest_anime(self):
        """test for latest anime."""
        self.assertIsInstance(self.latest_anime, myanimelist.anime.Anime)
        self.assertGreater(self.latest_anime.id, 20000)

    def test_anime_valid(self):
        """test if anime is valid."""
        self.assertIsInstance(self.bebop, myanimelist.anime.Anime)

    def test_title(self):
        """test title."""
        self.assertEqual(self.bebop.title, 'Cowboy Bebop')
        self.assertEqual(self.spicy_wolf.title, 'Ookami to Koushinryou')
        self.assertEqual(self.space_dandy.title, 'Space☆Dandy')
        self.assertEqual(self.prisma.title, 'Fate/kaleid liner Prisma☆Illya: Undoukai de Dance!')

    def test_picture(self):
        """test picture."""
        self.assertIsInstance(self.spicy_wolf.picture, unicode)
        self.assertIsInstance(self.space_dandy.picture, unicode)
        self.assertIsInstance(self.bebop.picture, unicode)
        self.assertIsInstance(self.totoro.picture, unicode)
        self.assertIsInstance(self.prisma.picture, unicode)

    def test_alternative_titles(self):
        """test alternative title."""
        self.assertIn('Japanese', self.bebop.alternative_titles)
        self.assertIsInstance(self.bebop.alternative_titles['Japanese'], list)

        self.assertIn('English', self.spicy_wolf.alternative_titles)
        self.assertIsInstance(self.spicy_wolf.alternative_titles['English'], list)
        self.assertIn('Spice and Wolf', self.spicy_wolf.alternative_titles['English'])

        self.assertIn('Japanese', self.space_dandy.alternative_titles)
        self.assertIsInstance(self.space_dandy.alternative_titles['Japanese'], list)

        self.assertIn('Japanese', self.prisma.alternative_titles)
        self.assertIsInstance(self.prisma.alternative_titles['Japanese'], list)
        self.assertIn('カウボーイビバップ', self.bebop.alternative_titles['Japanese'])
        self.assertIn('スペース☆ダンディ', self.space_dandy.alternative_titles['Japanese'])
        self.assertIn(
            'Fate/kaleid liner プリズマ☆イリヤ 運動会 DE ダンス!',
            self.prisma.alternative_titles['Japanese']
        )

    def test_types(self):
        """test type."""
        self.assertEqual(self.bebop.type, 'TV')
        self.assertEqual(self.totoro.type, 'Movie')
        self.assertEqual(self.prisma.type, 'OVA')

    def test_episodes(self):
        """ test episode."""
        self.assertEqual(self.spicy_wolf.episodes, 13)
        self.assertEqual(self.bebop.episodes, 26)
        self.assertEqual(self.totoro.episodes, 1)
        self.assertEqual(self.space_dandy.episodes, 13)
        self.assertEqual(self.prisma.episodes, 1)

    def test_status(self):
        """ test status."""
        self.assertEqual(self.spicy_wolf.status, 'Finished Airing')
        self.assertEqual(self.totoro.status, 'Finished Airing')
        self.assertEqual(self.bebop.status, 'Finished Airing')
        self.assertEqual(self.space_dandy.status, 'Finished Airing')
        self.assertEqual(self.prisma.status, 'Finished Airing')

    def test_aired(self):
        """test airing date."""
        self.assertEqual(self.spicy_wolf.aired,
                         (datetime.date(month=1, day=8, year=2008), datetime.date(month=5, day=30,
                                                                                  year=2008)))
        self.assertEqual(self.bebop.aired,
                         (datetime.date(month=4, day=3, year=1998), datetime.date(month=4, day=24,
                                                                                  year=1999)))
        self.assertEqual(self.space_dandy.aired,
                         (datetime.date(month=1, day=5, year=2014), datetime.date(month=3, day=27,
                                                                                  year=2014)))
        self.assertEqual(self.totoro.aired, (datetime.date(month=4, day=16, year=1988),))
        self.assertGreaterEqual(self.prisma.aired, (datetime.date(month=3, day=10, year=2014),))

    def test_producers(self):
        """test producer."""
        self.assertIsInstance(self.bebop.producers, list)
        self.assertGreater(len(self.bebop.producers), 0)

        self.assertIn(self.bandai_visual, self.bebop.producers)

        self.assertIsInstance(self.spicy_wolf.producers, list)
        self.assertGreater(len(self.spicy_wolf.producers), 0)

        self.assertIn(self.kadokawa, self.spicy_wolf.producers)

        self.assertIsInstance(self.space_dandy.producers, list)
        self.assertGreater(len(self.space_dandy.producers), 0)

        self.assertIn(self.bandai_visual, self.space_dandy.producers)

        self.assertIsInstance(self.totoro.producers, list)
        self.assertGreater(len(self.totoro.producers), 0)

        self.assertIn(self.studio_fantasia, self.totoro.producers)

        self.assertIsInstance(self.prisma.producers, list)
        self.assertGreaterEqual(len(self.prisma.producers), 0)

    def test_genres(self):
        """test genres."""
        self.assertIsInstance(self.bebop.genres, list)
        self.assertGreater(len(self.bebop.genres), 0)
        self.assertIn(self.action, self.bebop.genres)
        self.assertIsInstance(self.spicy_wolf.genres, list)
        self.assertGreater(len(self.spicy_wolf.genres), 0)

        self.assertIn(self.romance, self.spicy_wolf.genres)
        self.assertIsInstance(self.space_dandy.genres, list)
        self.assertGreater(len(self.space_dandy.genres), 0)

        self.assertIn(self.scifi, self.space_dandy.genres)
        self.assertIsInstance(self.totoro.genres, list)
        self.assertGreater(len(self.totoro.genres), 0)

        self.assertIn(self.supernatural, self.totoro.genres)
        self.assertIsInstance(self.prisma.genres, list)
        self.assertGreater(len(self.prisma.genres), 0)
        self.assertIn(self.fantasy, self.prisma.genres)

    def test_duration(self):
        """test duration."""
        self.assertEqual(self.spicy_wolf.duration.total_seconds(), 1440)
        self.assertEqual(self.totoro.duration.total_seconds(), 5160)
        self.assertEqual(self.space_dandy.duration.total_seconds(), 1440)
        self.assertEqual(self.bebop.duration.total_seconds(), 1440)
        self.assertEqual(self.prisma.duration.total_seconds(), 1500)

    def test_score(self):
        """test score"""
        self.assertIsInstance(self.spicy_wolf.score, tuple)
        self.assertGreater(self.spicy_wolf.score[0], 0)
        self.assertLess(self.spicy_wolf.score[0], 10)
        self.assertIsInstance(self.spicy_wolf.score[1], int)
        self.assertGreaterEqual(self.spicy_wolf.score[1], 0)
        self.assertIsInstance(self.bebop.score, tuple)
        self.assertGreater(self.bebop.score[0], 0)
        self.assertLess(self.bebop.score[0], 10)
        self.assertIsInstance(self.bebop.score[1], int)
        self.assertGreaterEqual(self.bebop.score[1], 0)
        self.assertIsInstance(self.space_dandy.score, tuple)
        self.assertGreater(self.space_dandy.score[0], 0)
        self.assertLess(self.space_dandy.score[0], 10)
        self.assertIsInstance(self.space_dandy.score[1], int)
        self.assertGreaterEqual(self.space_dandy.score[1], 0)
        self.assertIsInstance(self.totoro.score, tuple)
        self.assertGreater(self.totoro.score[0], 0)
        self.assertLess(self.totoro.score[0], 10)
        self.assertIsInstance(self.totoro.score[1], int)
        self.assertGreaterEqual(self.totoro.score[1], 0)
        self.assertGreater(self.prisma.score[0], 0)
        self.assertLess(self.prisma.score[0], 10)
        self.assertIsInstance(self.prisma.score[1], int)
        self.assertGreaterEqual(self.prisma.score[1], 0)

    def test_rank(self):
        """test rank."""
        self.assertIsInstance(self.spicy_wolf.rank, int)
        self.assertGreater(self.spicy_wolf.rank, 0)
        self.assertIsInstance(self.bebop.rank, int)
        self.assertGreater(self.bebop.rank, 0)
        self.assertIsInstance(self.space_dandy.rank, int)
        self.assertGreater(self.space_dandy.rank, 0)
        self.assertIsInstance(self.totoro.rank, int)
        self.assertGreater(self.totoro.rank, 0)
        self.assertIsInstance(self.prisma.rank, int)
        self.assertGreater(self.prisma.rank, 0)

    def test_popularity(self):
        """test popularity."""
        self.assertIsInstance(self.spicy_wolf.popularity, int)
        self.assertGreater(self.spicy_wolf.popularity, 0)
        self.assertIsInstance(self.bebop.popularity, int)
        self.assertGreater(self.bebop.popularity, 0)
        self.assertIsInstance(self.space_dandy.popularity, int)
        self.assertGreater(self.space_dandy.popularity, 0)
        self.assertIsInstance(self.totoro.popularity, int)
        self.assertGreater(self.totoro.popularity, 0)
        self.assertIsInstance(self.prisma.popularity, int)
        self.assertGreater(self.prisma.popularity, 0)

    def test_members(self):
        """test members."""
        self.assertIsInstance(self.spicy_wolf.members, int)
        self.assertGreater(self.spicy_wolf.members, 0)
        self.assertIsInstance(self.bebop.members, int)
        self.assertGreater(self.bebop.members, 0)
        self.assertIsInstance(self.space_dandy.members, int)
        self.assertGreater(self.space_dandy.members, 0)
        self.assertIsInstance(self.totoro.members, int)
        self.assertGreater(self.totoro.members, 0)
        self.assertIsInstance(self.prisma.members, int)
        self.assertGreater(self.prisma.members, 0)

    def test_favorites(self):
        """test favorites."""
        self.assertIsInstance(self.spicy_wolf.favorites, int)
        self.assertGreater(self.spicy_wolf.favorites, 0)
        self.assertIsInstance(self.bebop.favorites, int)
        self.assertGreater(self.bebop.favorites, 0)
        self.assertIsInstance(self.space_dandy.favorites, int)
        self.assertGreater(self.space_dandy.favorites, 0)
        self.assertIsInstance(self.totoro.favorites, int)
        self.assertGreater(self.totoro.favorites, 0)
        self.assertIsInstance(self.prisma.favorites, int)
        self.assertGreater(self.prisma.favorites, 0)

    def test_synopsis(self):
        """test synopsis."""
        self.assertIsInstance(self.spicy_wolf.synopsis, unicode)
        self.assertGreater(len(self.spicy_wolf.synopsis), 0)
        self.assertIn('Holo', self.spicy_wolf.synopsis)
        # check if background-part not synopsis
        self.assertNotIn('No background information has been added to this title.',
                         self.spicy_wolf.synopsis)

        self.assertIsInstance(self.bebop.synopsis, unicode)
        self.assertGreater(len(self.bebop.synopsis), 0)
        self.assertIn('Spike', self.bebop.synopsis)
        self.assertIsInstance(self.space_dandy.synopsis, unicode)
        self.assertGreater(len(self.space_dandy.synopsis), 0)
        self.assertIn('dandy', self.space_dandy.synopsis)
        self.assertIsInstance(self.totoro.synopsis, unicode)
        self.assertGreater(len(self.totoro.synopsis), 0)
        self.assertIn('Satsuki', self.totoro.synopsis)
        self.assertIsInstance(self.prisma.synopsis, unicode)
        self.assertGreater(len(self.prisma.synopsis), 0)
        self.assertIn('Illya', self.prisma.synopsis)

    def test_related(self):
        """test related."""
        self.assertIsInstance(self.spicy_wolf.related, dict)
        self.assertIn('Sequel', self.spicy_wolf.related)
        self.assertIn(self.spicy_wolf_sequel, self.spicy_wolf.related['Sequel'])
        self.assertIsInstance(self.bebop.related, dict)
        self.assertIn('Side story', self.bebop.related)
        self.assertIn(self.bebop_side_story, self.bebop.related['Side story'])

    def test_characters(self):
        """test characters."""
        self.assertIsInstance(self.spicy_wolf.characters, dict)
        self.assertGreater(len(self.spicy_wolf.characters), 0)
        self.assertIn(self.holo, self.spicy_wolf.characters)
        self.assertEqual(self.spicy_wolf.characters[self.holo]['role'], 'Main')
        self.assertIn(self.holo_va, self.spicy_wolf.characters[self.holo]['voice_actors'])

        self.assertIsInstance(self.bebop.characters, dict)
        self.assertGreater(len(self.bebop.characters), 0)

        self.assertIn(self.hex, self.bebop.characters)
        self.assertEqual(self.bebop.characters[self.hex]['role'], 'Supporting')
        self.assertIn(self.hex_va, self.bebop.characters[self.hex]['voice_actors'])
        self.assertIsInstance(self.space_dandy.characters, dict)
        self.assertGreater(len(self.space_dandy.characters), 0)
        self.assertIn(self.toaster, self.space_dandy.characters)
        self.assertEqual(self.space_dandy.characters[self.toaster]['role'], 'Supporting')
        self.assertIn(self.toaster_va, self.space_dandy.characters[self.toaster]['voice_actors'])
        self.assertIsInstance(self.totoro.characters, dict)
        self.assertGreater(len(self.totoro.characters), 0)
        self.assertIn(self.satsuki, self.totoro.characters)
        self.assertEqual(self.totoro.characters[self.satsuki]['role'], 'Main')
        self.assertIn(self.satsuki_va, self.totoro.characters[self.satsuki]['voice_actors'])
        self.assertIsInstance(self.prisma.characters, dict)
        self.assertGreater(len(self.prisma.characters), 0)
        self.assertIn(self.ilya, self.prisma.characters)
        self.assertEqual(self.prisma.characters[self.ilya]['role'], 'Main')
        self.assertIn(self.ilya_va, self.prisma.characters[self.ilya]['voice_actors'])

    def test_voice_actors(self):
        """test voice actors."""
        self.assertIsInstance(self.spicy_wolf.voice_actors, dict)
        self.assertGreater(len(self.spicy_wolf.voice_actors), 0)
        self.assertIn(self.holo_va, self.spicy_wolf.voice_actors)
        self.assertEqual(self.spicy_wolf.voice_actors[self.holo_va]['role'], 'Main')
        self.assertEqual(self.spicy_wolf.voice_actors[self.holo_va]['character'], self.holo)
        self.assertIsInstance(self.bebop.voice_actors, dict)
        self.assertGreater(len(self.bebop.voice_actors), 0)
        self.assertIn(self.hex_va, self.bebop.voice_actors)
        self.assertEqual(self.bebop.voice_actors[self.hex_va]['role'], 'Supporting')
        self.assertEqual(self.bebop.voice_actors[self.hex_va]['character'], self.hex)
        self.assertIsInstance(self.space_dandy.voice_actors, dict)
        self.assertGreater(len(self.space_dandy.voice_actors), 0)
        self.assertIn(self.toaster_va, self.space_dandy.voice_actors)
        self.assertEqual(self.space_dandy.voice_actors[self.toaster_va]['role'], 'Supporting')
        self.assertEqual(self.space_dandy.voice_actors[self.toaster_va]['character'], self.toaster)
        self.assertIsInstance(self.totoro.voice_actors, dict)
        self.assertGreater(len(self.totoro.voice_actors), 0)
        self.assertIn(self.satsuki_va, self.totoro.voice_actors)
        self.assertEqual(self.totoro.voice_actors[self.satsuki_va]['role'], 'Main')
        self.assertEqual(self.totoro.voice_actors[self.satsuki_va]['character'], self.satsuki)
        self.assertIsInstance(self.prisma.voice_actors, dict)
        self.assertGreater(len(self.prisma.voice_actors), 0)
        self.assertIn(self.ilya_va, self.prisma.voice_actors)
        self.assertEqual(self.prisma.voice_actors[self.ilya_va][u'role'], 'Main')
        self.assertEqual(self.prisma.voice_actors[self.ilya_va][u'character'], self.ilya)

    def test_no_voice_actors(self):
        """test no voice actors."""
        self.assertIsInstance(self.non_non_biyori.voice_actors, dict)
        self.assertGreater(len(self.non_non_biyori.voice_actors), 0)
        # TODO L a method to check if a character not in va

    def test_staff(self):
        """test staff."""
        self.assertIsInstance(self.spicy_wolf.staff, dict)
        self.assertGreater(len(self.spicy_wolf.staff), 0)
        self.assertIn(self.session.person(472), self.spicy_wolf.staff)
        self.assertIn(u'Producer', self.spicy_wolf.staff[self.session.person(472)])
        self.assertIsInstance(self.bebop.staff, dict)
        self.assertGreater(len(self.bebop.staff), 0)
        self.assertIn(self.session.person(12221), self.bebop.staff)
        self.assertIn(u'Inserted Song Performance', self.bebop.staff[self.session.person(12221)])
        self.assertIsInstance(self.space_dandy.staff, dict)
        self.assertGreater(len(self.space_dandy.staff), 0)
        self.assertIn(self.session.person(10127), self.space_dandy.staff)

        for x in [u'Theme Song Composition', u'Theme Song Lyrics', u'Theme Song Performance']:
            self.assertIn(x, self.space_dandy.staff[self.session.person(10127)])
        self.assertIsInstance(self.totoro.staff, dict)
        self.assertGreater(len(self.totoro.staff), 0)
        self.assertIn(self.session.person(1870), self.totoro.staff)
        for x in [u'Director', u'Script', u'Storyboard']:
            self.assertIn(x, self.totoro.staff[self.session.person(1870)])
        self.assertIsInstance(self.prisma.staff, dict)
        self.assertGreater(len(self.prisma.staff), 0)
        self.assertIn(self.session.person(10617), self.prisma.staff)
        self.assertIn(u'ADR Director', self.prisma.staff[self.session.person(10617)])

    def test_popular_tags(self):
        """test popular tags."""
        self.assertGreater(len(self.bebop.popular_tags), 0)
        self.assertIn(self.space_tag, self.bebop.popular_tags)
        self.assertGreater(len(self.spicy_wolf.popular_tags), 0)
        self.assertIn(self.adventure_tag, self.spicy_wolf.popular_tags)
        self.assertEquals(len(self.non_tagged_anime.popular_tags), 1)
