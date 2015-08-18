#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase
import datetime

import myanimelist.session
import myanimelist.anime


class testAnimeClass(TestCase):
    @classmethod
    def setUpClass(self):
        self.session = myanimelist.session.Session()
        self.bebop = self.session.anime(1)
        self.sunrise = self.session.producer(14)
        self.action = self.session.genre(1)
        self.hex = self.session.character(94717)
        self.hex_va = self.session.person(5766)
        self.bebop_side_story = self.session.anime(5)
        self.space_tag = self.session.tag(u'space')

        self.spicy_wolf = self.session.anime(2966)
        self.kadokawa = self.session.producer(352)
        self.romance = self.session.genre(22)
        self.holo = self.session.character(7373)
        self.holo_va = self.session.person(70)
        self.spicy_wolf_sequel = self.session.anime(6007)
        self.adventure_tag = self.session.tag(u'adventure')

        self.space_dandy = self.session.anime(20057)
        self.funi = self.session.producer(102)
        self.scifi = self.session.genre(24)
        self.toaster = self.session.character(110427)
        self.toaster_va = self.session.person(611)

        self.totoro = self.session.anime(523)
        self.gkids = self.session.producer(783)
        self.supernatural = self.session.genre(37)
        self.satsuki = self.session.character(267)
        self.satsuki_va = self.session.person(1104)

        self.prisma = self.session.anime(18851)
        self.silver_link = self.session.producer(300)
        self.fantasy = self.session.genre(10)
        self.ilya = self.session.character(503)
        self.ilya_va = self.session.person(117)

        self.invalid_anime = self.session.anime(457384754)
        self.latest_anime = myanimelist.anime.Anime.newest(self.session)

        self.non_tagged_anime = self.session.anime(10448)
        # this anime is not non_tagged but only have one tag(drama)

    def testNoIDInvalidAnime(self):
        with self.assertRaises(TypeError):
            self.session.anime()

    def testNoSessionInvalidLatestAnime(self):
        with self.assertRaises(TypeError):
            myanimelist.anime.Anime.newest()

    def testNegativeInvalidAnime(self):
        with self.assertRaises(myanimelist.anime.InvalidAnimeError):
            self.session.anime(-1)

    def testFloatInvalidAnime(self):
        with self.assertRaises(myanimelist.anime.InvalidAnimeError):
            self.session.anime(1.5)

    def testNonExistentAnime(self):
        with self.assertRaises(myanimelist.anime.InvalidAnimeError):
            self.invalid_anime.load()

    def testLatestAnime(self):
        self.assertIsInstance(self.latest_anime, myanimelist.anime.Anime)
        self.assertGreater(self.latest_anime.id, 20000)

    def testAnimeValid(self):
        self.assertIsInstance(self.bebop, myanimelist.anime.Anime)

    def testTitle(self):
        self.assertEqual(self.bebop.title, u'Cowboy Bebop')
        self.assertEqual(self.spicy_wolf.title, u'Ookami to Koushinryou')
        self.assertEqual(self.space_dandy.title, u'Space☆Dandy')
        self.assertEqual(self.prisma.title, u'Fate/kaleid liner Prisma☆Illya: Undoukai de Dance!')

    def testPicture(self):
        self.assertIsInstance(self.spicy_wolf.picture, unicode)
        self.assertIsInstance(self.space_dandy.picture, unicode)
        self.assertIsInstance(self.bebop.picture, unicode)
        self.assertIsInstance(self.totoro.picture, unicode)
        self.assertIsInstance(self.prisma.picture, unicode)

    def testAlternativeTitles(self):
        self.assertIn(u'Japanese', self.bebop.alternative_titles)
        self.assertIsInstance(self.bebop.alternative_titles[u'Japanese'], list)
        self.assertIn(u'カウボーイビバップ', self.bebop.alternative_titles[u'Japanese'])

        self.assertIn(u'English', self.spicy_wolf.alternative_titles)
        self.assertIsInstance(self.spicy_wolf.alternative_titles[u'English'], list)
        self.assertIn(u'Spice and Wolf', self.spicy_wolf.alternative_titles[u'English'])

        self.assertIn(u'Japanese', self.space_dandy.alternative_titles)
        self.assertIsInstance(self.space_dandy.alternative_titles[u'Japanese'], list)
        self.assertIn(u'スペース☆ダンディ', self.space_dandy.alternative_titles[u'Japanese'])

        self.assertIn(u'Japanese', self.prisma.alternative_titles)
        self.assertIsInstance(self.prisma.alternative_titles[u'Japanese'], list)
        self.assertIn(u'Fate/kaleid liner プリズマ☆イリヤ 運動会 DE ダンス!',
                      self.prisma.alternative_titles[u'Japanese'])

    def testTypes(self):
        self.assertEqual(self.bebop.type, u'TV')
        self.assertEqual(self.totoro.type, u'Movie')
        self.assertEqual(self.prisma.type, u'OVA')

    def testEpisodes(self):
        self.assertEqual(self.spicy_wolf.episodes, 13)
        self.assertEqual(self.bebop.episodes, 26)
        self.assertEqual(self.totoro.episodes, 1)
        self.assertEqual(self.space_dandy.episodes, 13)
        self.assertEqual(self.prisma.episodes, 1)

    def testStatus(self):
        self.assertEqual(self.spicy_wolf.status, u'Finished Airing')
        self.assertEqual(self.totoro.status, u'Finished Airing')
        self.assertEqual(self.bebop.status, u'Finished Airing')
        self.assertEqual(self.space_dandy.status, u'Finished Airing')
        self.assertEqual(self.prisma.status, u'Finished Airing')

    def testAired(self):
        self.assertEqual(self.spicy_wolf.aired, 
                         (datetime.date(month=1, day=8, year=2008), datetime.date(month=5, day=30, year=2008)))
        self.assertEqual(self.bebop.aired,
                         (datetime.date(month=4, day=3, year=1998), datetime.date(month=4, day=24, year=1999)))
        self.assertEqual(self.space_dandy.aired,
                         (datetime.date(month=1, day=5, year=2014), datetime.date(month=3, day=27, year=2014)))
        self.assertEqual(self.totoro.aired, (datetime.date(month=4, day=16, year=1988),))
        self.assertEqual(self.prisma.aired, (datetime.date(month=3, day=10, year=2014),))

    def testProducers(self):
        self.assertIsInstance(self.bebop.producers, list)
        self.assertGreater(len(self.bebop.producers), 0)

        self.assertIn(self.sunrise, self.bebop.producers)

        self.assertIsInstance(self.spicy_wolf.producers, list)
        self.assertGreater(len(self.spicy_wolf.producers), 0)

        self.assertIn(self.kadokawa, self.spicy_wolf.producers)

        self.assertIsInstance(self.space_dandy.producers, list)
        self.assertGreater(len(self.space_dandy.producers), 0)

        self.assertIn(self.funi, self.space_dandy.producers)

        self.assertIsInstance(self.totoro.producers, list)
        self.assertGreater(len(self.totoro.producers), 0)

        self.assertIn(self.gkids, self.totoro.producers)

        self.assertIsInstance(self.prisma.producers, list)
        self.assertGreater(len(self.prisma.producers), 0)

        self.assertIn(self.silver_link, self.prisma.producers)

    def testGenres(self):
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

    def testDuration(self):
        self.assertEquals(self.spicy_wolf.duration.total_seconds(), 1440)
        self.assertEquals(self.totoro.duration.total_seconds(), 5160)
        self.assertEquals(self.space_dandy.duration.total_seconds(), 1440)
        self.assertEquals(self.bebop.duration.total_seconds(), 1440)
        self.assertEquals(self.prisma.duration.total_seconds(), 1500)

    def testScore(self):
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

    def testRank(self):
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

    def testPopularity(self):
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

    def testMembers(self):
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

    def testFavorites(self):
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

    def testSynopsis(self):
        self.assertIsInstance(self.spicy_wolf.synopsis, unicode)
        self.assertGreater(len(self.spicy_wolf.synopsis), 0)
        self.assertIn(u'Holo', self.spicy_wolf.synopsis)
        self.assertIsInstance(self.bebop.synopsis, unicode)
        self.assertGreater(len(self.bebop.synopsis), 0)
        self.assertIn(u'Spike', self.bebop.synopsis)
        self.assertIsInstance(self.space_dandy.synopsis, unicode)
        self.assertGreater(len(self.space_dandy.synopsis), 0)
        self.assertIn(u'dandy', self.space_dandy.synopsis)
        self.assertIsInstance(self.totoro.synopsis, unicode)
        self.assertGreater(len(self.totoro.synopsis), 0)
        self.assertIn(u'Satsuki', self.totoro.synopsis)
        self.assertIsInstance(self.prisma.synopsis, unicode)
        self.assertGreater(len(self.prisma.synopsis), 0)
        self.assertIn(u'Einzbern', self.prisma.synopsis)

    def testRelated(self):
        self.assertIsInstance(self.spicy_wolf.related, dict)
        self.assertIn('Sequel', self.spicy_wolf.related)
        self.assertIn(self.spicy_wolf_sequel, self.spicy_wolf.related[u'Sequel'])
        self.assertIsInstance(self.bebop.related, dict)
        self.assertIn('Side story', self.bebop.related)
        self.assertIn(self.bebop_side_story, self.bebop.related[u'Side story'])

    def testCharacters(self):
        self.assertIsInstance(self.spicy_wolf.characters, dict)
        self.assertGreater(len(self.spicy_wolf.characters), 0)
        self.assertIn(self.holo, self.spicy_wolf.characters)
        self.assertEqual(self.spicy_wolf.characters[self.holo][u'role'], 'Main')
        self.assertIn(self.holo_va, self.spicy_wolf.characters[self.holo][u'voice_actors'])

        self.assertIsInstance(self.bebop.characters, dict)
        self.assertGreater(len(self.bebop.characters), 0)

        self.assertIn(self.hex, self.bebop.characters)
        self.assertEqual(self.bebop.characters[self.hex][u'role'], 'Supporting')
        self.assertIn(self.hex_va, self.bebop.characters[self.hex][u'voice_actors'])
        self.assertIsInstance(self.space_dandy.characters, dict)
        self.assertGreater(len(self.space_dandy.characters), 0)
        self.assertIn(self.toaster, self.space_dandy.characters)
        self.assertEqual(self.space_dandy.characters[self.toaster][u'role'], 'Supporting')
        self.assertIn(self.toaster_va, self.space_dandy.characters[self.toaster][u'voice_actors'])
        self.assertIsInstance(self.totoro.characters, dict)
        self.assertGreater(len(self.totoro.characters), 0)
        self.assertIn(self.satsuki, self.totoro.characters)
        self.assertEqual(self.totoro.characters[self.satsuki][u'role'], 'Main')
        self.assertIn(self.satsuki_va, self.totoro.characters[self.satsuki][u'voice_actors'])
        self.assertIsInstance(self.prisma.characters, dict)
        self.assertGreater(len(self.prisma.characters), 0)
        self.assertIn(self.ilya, self.prisma.characters)
        self.assertEqual(self.prisma.characters[self.ilya][u'role'], 'Main')
        self.assertIn(self.ilya_va, self.prisma.characters[self.ilya][u'voice_actors'])

    def testVoiceActors(self):
        self.assertIsInstance(self.spicy_wolf.voice_actors, dict)
        self.assertGreater(len(self.spicy_wolf.voice_actors), 0)
        self.assertIn(self.holo_va, self.spicy_wolf.voice_actors)
        self.assertEqual(self.spicy_wolf.voice_actors[self.holo_va][u'role'], 'Main')
        self.assertEqual(self.spicy_wolf.voice_actors[self.holo_va][u'character'], self.holo)
        self.assertIsInstance(self.bebop.voice_actors, dict)
        self.assertGreater(len(self.bebop.voice_actors), 0)
        self.assertIn(self.hex_va, self.bebop.voice_actors)
        self.assertEqual(self.bebop.voice_actors[self.hex_va][u'role'], 'Supporting')
        self.assertEqual(self.bebop.voice_actors[self.hex_va][u'character'], self.hex)
        self.assertIsInstance(self.space_dandy.voice_actors, dict)
        self.assertGreater(len(self.space_dandy.voice_actors), 0)
        self.assertIn(self.toaster_va, self.space_dandy.voice_actors)
        self.assertEqual(self.space_dandy.voice_actors[self.toaster_va][u'role'], 'Supporting')
        self.assertEqual(self.space_dandy.voice_actors[self.toaster_va][u'character'], self.toaster)
        self.assertIsInstance(self.totoro.voice_actors, dict)
        self.assertGreater(len(self.totoro.voice_actors), 0)
        self.assertIn(self.satsuki_va, self.totoro.voice_actors)
        self.assertEqual(self.totoro.voice_actors[self.satsuki_va][u'role'], 'Main')
        self.assertEqual(self.totoro.voice_actors[self.satsuki_va][u'character'], self.satsuki)
        self.assertIsInstance(self.prisma.voice_actors, dict)
        self.assertGreater(len(self.prisma.voice_actors), 0)
        self.assertIn(self.ilya_va, self.prisma.voice_actors)
        self.assertEqual(self.prisma.voice_actors[self.ilya_va][u'role'], 'Main')
        self.assertEqual(self.prisma.voice_actors[self.ilya_va][u'character'], self.ilya)

    def testStaff(self):
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

    def testPopularTags(self):
        self.assertGreater(len(self.bebop.popular_tags), 0)
        self.assertIn(self.space_tag, self.bebop.popular_tags)
        self.assertGreater(len(self.spicy_wolf.popular_tags), 0)
        self.assertIn(self.adventure_tag, self.spicy_wolf.popular_tags)
        self.assertEquals(len(self.non_tagged_anime.popular_tags), 1)
