#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase
import datetime

import myanimelist.session
import myanimelist.user
from myanimelist.user import User

from nose.plugins.attrib import attr
from six import string_types


class testUserClass(TestCase):
    """class to test user module."""

    @classmethod
    def setUpClass(self):
        """set up for user test."""
        self.session = myanimelist.session.Session()
        self.shal = self.session.user('shaldengeki')
        self.gits = self.session.anime(467)
        self.clannad_as = self.session.anime(4181)
        self.tohsaka = self.session.character(498)
        self.fsn = self.session.anime(356)
        self.fujibayashi = self.session.character(4605)
        self.clannad_movie = self.session.anime(1723)
        self.fate_zero = self.session.anime(10087)
        self.bebop = self.session.anime(1)
        self.kanon = self.session.anime(1530)
        self.fang_tan_club = self.session.club(9560)
        self.satsuki_club = self.session.club(6246)

        self.mona = self.session.user('monausicaa')
        self.megami = self.session.manga(446)
        self.chobits = self.session.manga(107)
        self.kugimiya = self.session.person(8)
        self.kayano = self.session.person(10765)

        self.naruleach = self.session.user('Naruleach')
        self.mal_rewrite_club = self.session.club(6498)
        self.fantasy_anime_club = self.session.club(379)

        self.smooched = self.session.user('Smooched')
        self.sao = self.session.anime(11757)

        self.ziron = self.session.user('Ziron')
        self.seraph = self.session.user('seraphzero')
        self.threger = self.session.user('threger')
        self.archaeon = self.session.user('Archaeon')

        # NOTE 
        # shal account look like can't automatically get favorites list if not loading first
        self.shal.load()

    def testNoIDInvalidUser(self):
        with self.assertRaises(TypeError):
            self.session.user()

    def testNegativeInvalidUser(self):
        with self.assertRaises(myanimelist.user.InvalidUserError):
            self.session.user(-1)

    def testFloatInvalidUser(self):
        with self.assertRaises(myanimelist.user.InvalidUserError):
            self.session.user(1.5)

    def testNonExistentUser(self):
        with self.assertRaises(myanimelist.user.InvalidUserError):
            self.session.user(457384754).load()

    def testUserValid(self):
        self.assertIsInstance(self.shal, myanimelist.user.User)

    def test_id(self):
        """test user id."""
        self.assertEqual(self.shal.id, '64611')
        self.assertIsInstance(self.shal.id, string_types)
        self.assertEqual(self.mona.id, '244263')
        self.assertIsInstance(self.mona.id, string_types)

    def testUsername(self):
        self.assertEqual(self.shal.username, 'shaldengeki')
        self.assertEqual(self.mona.username, 'monausicaa')

    def test_picture(self):
        """test picture."""
        self.assertIsInstance(self.shal.picture, string_types)
        shal_pic = self.shal.picture
        self.assertIn(shal_pic[:7], ['http://', 'https:/'])
        self.assertEqual(shal_pic[-4:], '.jpg')
        self.assertIsInstance(self.mona.picture, string_types)

    def testFavoriteAnime(self):
        self.assertIsInstance(self.shal.favorite_anime, list)
        self.assertGreater(len(self.shal.favorite_anime), 0)
        self.assertIn(self.gits, self.shal.favorite_anime)
        self.assertIn(self.clannad_as, self.shal.favorite_anime)

        self.assertIsInstance(self.mona.favorite_anime, list)
        self.assertGreaterEqual(len(self.mona.favorite_anime), 0)

    def testFavoriteManga(self):
        self.assertIsInstance(self.shal.favorite_manga, list)
        self.assertEqual(len(self.shal.favorite_manga), 0)

        self.assertIsInstance(self.mona.favorite_manga, list)
        self.assertGreater(len(self.mona.favorite_manga), 0)
        self.assertIn(self.megami, self.mona.favorite_manga)
        self.assertIn(self.chobits, self.mona.favorite_manga)

    def testFavoriteCharacters(self):
        self.assertIsInstance(self.shal.favorite_characters, dict)
        self.assertGreater(len(self.shal.favorite_characters), 0)
        self.assertIn(self.tohsaka, self.shal.favorite_characters)
        self.assertIn(self.fujibayashi, self.shal.favorite_characters)
        self.assertEqual(self.shal.favorite_characters[self.tohsaka], self.fsn)
        self.assertEqual(self.shal.favorite_characters[self.fujibayashi], self.clannad_movie)

        self.assertIsInstance(self.mona.favorite_characters, dict)
        self.assertGreater(len(self.mona.favorite_characters), 0)

    def testFavoritePeople(self):
        self.assertIsInstance(self.shal.favorite_people, list)
        self.assertEqual(len(self.shal.favorite_people), 0)
        self.assertIsInstance(self.mona.favorite_people, list)
        self.assertGreater(len(self.mona.favorite_people), 0)
        self.assertIn(self.kugimiya, self.mona.favorite_people)
        self.assertIn(self.kayano, self.mona.favorite_people)

    def testLastOnline(self):
        self.assertIsInstance(self.shal.last_online, datetime.datetime)
        self.assertIsInstance(self.mona.last_online, datetime.datetime)

    def testGender(self):
        self.assertEqual(self.shal.gender, u"Not specified")
        self.assertEqual(self.mona.gender, "Male")

    def testBirthday(self):
        self.assertIsInstance(self.shal.birthday, datetime.date)
        self.assertEqual(self.shal.birthday, datetime.date(year=1989, month=11, day=5))

        self.assertIsInstance(self.mona.birthday, datetime.date)
        self.assertEqual(self.mona.birthday, datetime.date(year=1991, month=8, day=11))

    def testLocation(self):
        self.assertEqual(self.shal.location, 'Chicago, IL')
        self.assertIsInstance(self.mona.location, string_types)

    def testWebsite(self):
        self.assertEqual(self.shal.website, 'llanim.us')
        self.assertIsNone(self.mona.website)

    def testJoinDate(self):
        self.assertIsInstance(self.shal.join_date, datetime.date)
        self.assertEqual(self.shal.join_date, datetime.date(year=2008, month=5, day=30))
        self.assertIsInstance(self.mona.join_date, datetime.date)
        self.assertEqual(self.mona.join_date, datetime.date(year=2009, month=10, day=9))

    def testAccessRank(self):
        self.assertEqual(self.shal.access_rank, 'Member')
        self.assertEqual(self.mona.access_rank, 'Member')
        self.assertEqual(self.naruleach.access_rank, 'Anime DB Moderator')

    def testAnimeListViews(self):
        """
        test anime list.

        .. deprecated:: 0.1.8
            Anime list test is not available anymore.
        """
        pass

    def testMangaListViews(self):
        """
        test manga list.

        .. deprecated:: 0.1.8
            Manga list test is not available anymore.
        """
        pass

    def testNumComments(self):
        self.assertIsInstance(self.shal.num_comments, int)
        self.assertGreaterEqual(self.shal.num_comments, 72)

        self.assertIsInstance(self.mona.num_comments, int)
        self.assertGreaterEqual(self.mona.num_comments, 24)

    def testNumForumPosts(self):
        self.assertIsInstance(self.shal.num_forum_posts, int)
        self.assertGreaterEqual(self.shal.num_forum_posts, 5)
        self.assertIsInstance(self.mona.num_forum_posts, int)
        self.assertGreaterEqual(self.mona.num_forum_posts, 1)

    def test_parse_update_media_status(self):
        data = [
            (
                ('\n            Watching\n                        6/13\n                    ·'
                '             Scored\n      -'),
                {'episodes': 6, 'status': 'Watching', 'total_episodes': 13}
            ),
            (
                ('\n            Watching\n                        2/13\n                    ·'
                '             Scored\n      -'),
                {'episodes': 2, 'status': 'Watching', 'total_episodes': 13}
            ),
            (
                ('\n            Completed\n                        26/26\n                    ·'
                '             Scored\n      9'),
                {'episodes': 26, 'score': 9, 'total_episodes': 26, 'status': 'Completed'}
            ),
            (
                ('\n            Completed\n                        4/4\n                    ·'
                '             Scored\n      9'),
                {'episodes': 4, 'score': 9, 'total_episodes': 4, 'status': 'Completed'}
            ),
            (
                ('\n            Dropped\n                        73/116\n                    ·'
                '             Scored\n      6'),
                {'episodes': 73, 'score': 6, 'total_episodes': 116, 'status': 'Dropped'}
            ),

            (
                ('\n            Watching\n                        10/12\n                    ·'
                '             Scored\n      -'),
                {'episodes': 10, 'status': 'Watching', 'total_episodes': 12}
            ),
            (
                ('\n            Watching\n                        10/12\n                    ·'
                '             Scored\n      -'),
                {'episodes': 10, 'status': 'Watching', 'total_episodes': 12}
            ),
            (
                ('\n            Watching\n                        6/26\n                    ·'
                '             Scored\n      -'),
                {'episodes': 6, 'status': 'Watching', 'total_episodes': 26}
            ),
            (
                ('\n            Completed\n                        12/12\n                    ·'
                '             Scored\n      9'),
                {'episodes': 12, 'score': 9, 'total_episodes': 12, 'status': 'Completed'}
            ),
            (
                ('\n            Reading\n                        6/18\n                    ·'
                '             Scored\n      -'),
                {'episodes': 6, 'status': 'Reading', 'total_episodes': 18}
            ),
            (
                ('\n            Plan to Read\n            ·'
                '             Scored\n      -'),
                {'episodes': 0, 'status': 'Plan To Read', 'total_episodes': 0}
            )
        ]
        for item in data:
            # result = User._parse_update_media_status(item[0])
            # NOTE: can't access static method without giving TypeError
            result = self.shal._parse_update_media_status(item[0])
            self.assertDictEqual(result, item[1])

    def testLastListUpdates(self):
        self.assertIsInstance(self.shal.last_list_updates, dict)
        self.assertGreater(len(self.shal.last_list_updates), 0)
        self.assertIn(self.fate_zero, self.shal.last_list_updates)
        self.assertIn(self.bebop, self.shal.last_list_updates)
        self.assertEqual(self.shal.last_list_updates[self.fate_zero]['status'], 'Watching')
        self.assertEqual(self.shal.last_list_updates[self.fate_zero]['episodes'], 6)
        self.assertEqual(self.shal.last_list_updates[self.fate_zero]['total_episodes'], 13)
        self.assertIsInstance(self.shal.last_list_updates[self.fate_zero]['time'], datetime.datetime)
        self.assertEqual(self.shal.last_list_updates[self.fate_zero]['time'],
                         datetime.datetime(year=2014, month=9, day=5, hour=14, minute=1, second=0))
        self.assertIn(self.bebop, self.shal.last_list_updates)
        self.assertEqual(self.shal.last_list_updates[self.bebop]['status'], 'Completed')
        self.assertEqual(self.shal.last_list_updates[self.bebop]['episodes'], 26)
        self.assertEqual(self.shal.last_list_updates[self.bebop]['total_episodes'], 26)
        self.assertIsInstance(self.shal.last_list_updates[self.bebop]['time'], datetime.datetime)
        self.assertEqual(self.shal.last_list_updates[self.bebop]['time'],
                         datetime.datetime(year=2012, month=8, day=20, hour=11, minute=56, second=0))

        self.assertIsInstance(self.mona.last_list_updates, dict)
        self.assertGreater(len(self.mona.last_list_updates), 0)

    def testAnimeStats(self):
        self.assertIsInstance(self.shal.anime_stats, dict)
        self.assertGreater(len(self.shal.anime_stats), 0)
        self.assertEqual(self.shal.anime_stats[u'Days'], 38.9)
        self.assertEqual(self.shal.anime_stats[u'Total Entries'], 146)

        self.assertIsInstance(self.mona.anime_stats, dict)
        self.assertGreater(len(self.mona.anime_stats), 0)
        self.assertGreaterEqual(self.mona.anime_stats['Days'], 470)
        self.assertGreaterEqual(self.mona.anime_stats['Total Entries'], 1822)

    def testMangaStats(self):
        self.assertIsInstance(self.shal.manga_stats, dict)
        self.assertGreater(len(self.shal.manga_stats), 0)
        self.assertEqual(self.shal.manga_stats['Days'], 1.0)
        self.assertEqual(self.shal.manga_stats['Total Entries'], 2)
        self.assertIsInstance(self.mona.manga_stats, dict)
        self.assertGreater(len(self.mona.manga_stats), 0)
        self.assertGreaterEqual(self.mona.manga_stats['Days'], 69.4)
        self.assertGreaterEqual(self.mona.manga_stats['Total Entries'], 186)

    def testAbout(self):
        self.assertIsInstance(self.shal.about, string_types)
        self.assertGreater(len(self.shal.about), 0)
        self.assertIn(u'retiree', self.shal.about)
        self.assertIsNone(self.mona.about)

    @attr('slow')
    def testReviews(self):
        """test user reviews."""
        self.assertIsInstance(self.shal.reviews, dict)
        self.assertEqual(len(self.shal.reviews), 0)

        # not using smooched as test because (s)he delete all the review
        self.assertIsInstance(self.smooched.reviews, dict)
        self.assertGreaterEqual(len(self.smooched.reviews), 0)

        # NOTE: may have to change archaeon test to someone with less review to short the test time
        self.assertIsInstance(self.archaeon.reviews, dict)
        self.assertGreaterEqual(len(self.archaeon.reviews), 0)
        self.assertIn(self.fate_zero, self.archaeon.reviews)
        self.assertIsInstance(self.archaeon.reviews[self.fate_zero][u'date'], datetime.date)
        self.assertEqual(
            self.archaeon.reviews[self.fate_zero][u'date'],
            datetime.date(year=2012, month=1, day=14)
        )
        self.assertGreaterEqual(self.archaeon.reviews[self.fate_zero][u'people_helped'], 689)
        self.assertIsNone(self.archaeon.reviews[self.fate_zero][u'people_total'])
        self.assertEqual(self.archaeon.reviews[self.fate_zero][u'media_consumed'], 13)
        self.assertEqual(self.archaeon.reviews[self.fate_zero][u'media_total'], 13)
        self.assertEqual(self.archaeon.reviews[self.fate_zero][u'rating'], 9)
        self.assertIsInstance(self.archaeon.reviews[self.fate_zero][u'text'], string_types)
        self.assertGreater(len(self.archaeon.reviews[self.fate_zero][u'text']), 0)

        self.assertIsInstance(self.archaeon.reviews[self.fate_zero]['date'], datetime.date)
        self.assertEqual(self.archaeon.reviews[self.fate_zero]['date'],
                         datetime.date(year=2012, month=1, day=14))
        self.assertGreaterEqual(self.archaeon.reviews[self.fate_zero]['people_helped'], 689)
        self.assertIsNone(self.archaeon.reviews[self.fate_zero]['people_total'])

        self.assertEqual(self.archaeon.reviews[self.fate_zero]['media_consumed'], 13)
        self.assertEqual(self.archaeon.reviews[self.fate_zero]['media_total'], 13)
        self.assertEqual(self.archaeon.reviews[self.fate_zero]['rating'], 9)

        self.assertIsInstance(self.archaeon.reviews[self.fate_zero]['text'], string_types)
        self.assertGreater(len(self.archaeon.reviews[self.fate_zero]['text']), 0)

        self.assertIsInstance(self.threger.reviews, dict)
        self.assertEqual(len(self.threger.reviews), 0)

    def testRecommendations(self):
        self.assertIsInstance(self.shal.recommendations, dict)
        self.assertGreater(len(self.shal.recommendations), 0)
        self.assertIn(self.kanon, self.shal.recommendations)
        self.assertEqual(self.shal.recommendations[self.kanon][u'anime'], self.clannad_as)
        self.assertIsInstance(self.shal.recommendations[self.kanon][u'date'], datetime.date)
        self.assertEqual(
            self.shal.recommendations[self.kanon][u'date'],
            datetime.date(year=2009, month=3, day=13)
        )
        self.assertIsInstance(self.shal.recommendations[self.kanon][u'text'], string_types)
        self.assertGreater(len(self.shal.recommendations[self.kanon][u'text']), 0)

        self.assertIsInstance(self.mona.recommendations, dict)
        self.assertGreaterEqual(len(self.mona.recommendations), 0)

        self.assertIsInstance(self.naruleach.recommendations, dict)
        self.assertGreaterEqual(len(self.naruleach.recommendations), 0)

        self.assertIsInstance(self.threger.recommendations, dict)
        self.assertEqual(len(self.threger.recommendations), 0)

    def testClubs(self):
        self.assertIsInstance(self.shal.clubs, list)
        self.assertEqual(len(self.shal.clubs), 7)
        self.assertIn(self.fang_tan_club, self.shal.clubs)
        self.assertIn(self.satsuki_club, self.shal.clubs)
        self.assertIsInstance(self.naruleach.clubs, list)
        self.assertGreaterEqual(len(self.naruleach.clubs), 15)
        self.assertIn(self.mal_rewrite_club, self.naruleach.clubs)
        self.assertIn(self.fantasy_anime_club, self.naruleach.clubs)
        self.assertIsInstance(self.threger.clubs, list)
        self.assertEqual(len(self.threger.clubs), 0)

    def testFriends(self):
        self.assertIsInstance(self.shal.friends, dict)
        self.assertGreaterEqual(len(self.shal.friends), 31)
        self.assertIn(self.ziron, self.shal.friends)
        self.assertIsInstance(self.shal.friends[self.ziron]['last_active'], datetime.datetime)
        self.assertIn(self.ziron, self.shal.friends)
        self.assertIsInstance(self.shal.friends[self.ziron]['last_active'], datetime.datetime)
        self.assertIn(self.seraph, self.shal.friends)
        self.assertIsInstance(self.shal.friends[self.seraph]['last_active'], datetime.datetime)
        self.assertEqual(self.shal.friends[self.seraph]['since'],
                         datetime.datetime(year=2012, month=10, day=13, hour=19, minute=31, second=0))
        self.assertIsInstance(self.mona.friends, dict)
        self.assertGreaterEqual(len(self.mona.friends), 0)
        self.assertIsInstance(self.threger.friends, dict)
        self.assertEqual(len(self.threger.friends), 0)
