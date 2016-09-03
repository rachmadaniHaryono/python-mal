#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase
import datetime

import myanimelist.session
import myanimelist.user
from myanimelist.base import basestring, unicode


class testUserClass(TestCase):
    @classmethod
    def setUpClass(self):
        self.session = myanimelist.session.Session()
        self.shal = self.session.user(u'shaldengeki')
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

        self.ziron = self.session.user(u'Ziron')
        self.seraph = self.session.user(u'seraphzero')

        self.mona = self.session.user(u'monausicaa')
        self.megami = self.session.manga(446)
        self.chobits = self.session.manga(107)
        self.kugimiya = self.session.person(8)
        self.kayano = self.session.person(10765)

        self.naruleach = self.session.user(u'Naruleach')
        self.mal_rewrite_club = self.session.club(6498)
        self.fantasy_anime_club = self.session.club(379)

        self.smooched = self.session.user(u'Smooched')
        self.sao = self.session.anime(11757)
        self.threger = self.session.user(u'threger')

        self.archaeon = self.session.user(u'Archaeon')

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
        self.assertIsInstance(self.shal.id, basestring)
        self.assertEqual(self.mona.id, '244263')
        self.assertIsInstance(self.mona.id, basestring)

    def testUsername(self):
        self.assertEqual(self.shal.username, u'shaldengeki')
        self.assertEqual(self.mona.username, u'monausicaa')

    def test_picture(self):
        """test picture."""
        self.assertIsInstance(self.shal.picture, unicode)
        shal_pic = self.shal.picture
        self.assertIn(shal_pic[:7], ['http://', 'https:/'])
        self.assertEqual(shal_pic[-4:], '.jpg')
        self.assertIsInstance(self.mona.picture, unicode)

    def testFavoriteAnime(self):
        self.assertIsInstance(self.shal.favorite_anime, list)
        self.assertGreater(len(self.shal.favorite_anime), 0)
        self.assertIn(self.gits, self.shal.favorite_anime)
        self.assertIn(self.clannad_as, self.shal.favorite_anime)
        self.assertIsInstance(self.mona.favorite_anime, list)
        self.assertGreater(len(self.mona.favorite_anime), 0)

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
        self.assertEqual(self.mona.gender, u"Male")

    def testBirthday(self):
        self.assertIsInstance(self.shal.birthday, datetime.date)
        self.assertEqual(self.shal.birthday, datetime.date(year=1989, month=11, day=5))
        self.assertIsInstance(self.mona.birthday, datetime.date)
        self.assertEqual(self.mona.birthday, datetime.date(year=1991, month=8, day=11))

    def testLocation(self):
        self.assertEqual(self.shal.location, u'Chicago, IL')
        self.assertIsInstance(self.mona.location, unicode)

    def testWebsite(self):
        self.assertEqual(self.shal.website, u'llanim.us')
        self.assertIsNone(self.mona.website)

    def testJoinDate(self):
        self.assertIsInstance(self.shal.join_date, datetime.date)
        self.assertEqual(self.shal.join_date, datetime.date(year=2008, month=5, day=30))
        self.assertIsInstance(self.mona.join_date, datetime.date)
        self.assertEqual(self.mona.join_date, datetime.date(year=2009, month=10, day=9))

    def testAccessRank(self):
        self.assertEqual(self.shal.access_rank, u'Member')
        self.assertEqual(self.mona.access_rank, u'Member')
        self.assertEqual(self.naruleach.access_rank, u'Anime DB Moderator')

    def testAnimeListViews(self):
        self.assertIsInstance(self.shal.anime_list_views, int)
        self.assertGreaterEqual(self.shal.anime_list_views, 1767)
        self.assertIsInstance(self.mona.anime_list_views, int)
        self.assertGreaterEqual(self.mona.anime_list_views, 1969)

    def testMangaListViews(self):
        self.assertIsInstance(self.shal.manga_list_views, int)
        self.assertGreaterEqual(self.shal.manga_list_views, 1037)
        self.assertIsInstance(self.mona.manga_list_views, int)
        self.assertGreaterEqual(self.mona.manga_list_views, 548)

    def testNumComments(self):
        self.assertIsInstance(self.shal.num_comments, int)
        self.assertGreaterEqual(self.shal.num_comments, 93)
        self.assertIsInstance(self.mona.num_comments, int)
        self.assertGreaterEqual(self.mona.num_comments, 30)

    def testNumForumPosts(self):
        self.assertIsInstance(self.shal.num_forum_posts, int)
        self.assertGreaterEqual(self.shal.num_forum_posts, 5)
        self.assertIsInstance(self.mona.num_forum_posts, int)
        self.assertGreaterEqual(self.mona.num_forum_posts, 1)

    def testLastListUpdates(self):
        self.assertIsInstance(self.shal.last_list_updates, dict)
        self.assertGreater(len(self.shal.last_list_updates), 0)
        self.assertIn(self.fate_zero, self.shal.last_list_updates)
        self.assertIn(self.bebop, self.shal.last_list_updates)
        self.assertEqual(self.shal.last_list_updates[self.fate_zero][u'status'], u'Watching')
        self.assertEqual(self.shal.last_list_updates[self.fate_zero][u'episodes'], 6)
        self.assertEqual(self.shal.last_list_updates[self.fate_zero][u'total_episodes'], 13)
        self.assertIsInstance(self.shal.last_list_updates[self.fate_zero][u'time'], datetime.datetime)
        self.assertEqual(self.shal.last_list_updates[self.fate_zero][u'time'],
                         datetime.datetime(year=2014, month=9, day=5, hour=14, minute=1, second=0))
        self.assertIn(self.bebop, self.shal.last_list_updates)
        self.assertIn(self.bebop, self.shal.last_list_updates)
        self.assertEqual(self.shal.last_list_updates[self.bebop][u'status'], u'Completed')
        self.assertEqual(self.shal.last_list_updates[self.bebop][u'episodes'], 26)
        self.assertEqual(self.shal.last_list_updates[self.bebop][u'total_episodes'], 26)
        self.assertIsInstance(self.shal.last_list_updates[self.bebop][u'time'], datetime.datetime)
        self.assertEqual(self.shal.last_list_updates[self.bebop][u'time'],
                         datetime.datetime(year=2012, month=8, day=20, hour=11, minute=56, second=0))
        self.assertIsInstance(self.mona.last_list_updates, dict)
        self.assertGreater(len(self.mona.last_list_updates), 0)

    def testAnimeStats(self):
        self.assertIsInstance(self.shal.anime_stats, dict)
        self.assertGreater(len(self.shal.anime_stats), 0)
        self.assertEqual(self.shal.anime_stats[u'Time (Days)'], 38.9)
        self.assertEqual(self.shal.anime_stats[u'Total Entries'], 146)
        self.assertIsInstance(self.mona.anime_stats, dict)
        self.assertGreater(len(self.mona.anime_stats), 0)
        self.assertGreaterEqual(self.mona.anime_stats[u'Time (Days)'], 470)
        self.assertGreaterEqual(self.mona.anime_stats[u'Total Entries'], 1822)

    def testMangaStats(self):
        self.assertIsInstance(self.shal.manga_stats, dict)
        self.assertGreater(len(self.shal.manga_stats), 0)
        self.assertEqual(self.shal.manga_stats[u'Time (Days)'], 1.0)
        self.assertEqual(self.shal.manga_stats[u'Total Entries'], 2)
        self.assertIsInstance(self.mona.manga_stats, dict)
        self.assertGreater(len(self.mona.manga_stats), 0)
        self.assertGreaterEqual(self.mona.manga_stats[u'Time (Days)'], 69.4)
        self.assertGreaterEqual(self.mona.manga_stats[u'Total Entries'], 186)

    def testAbout(self):
        self.assertIsInstance(self.shal.about, unicode)
        self.assertGreater(len(self.shal.about), 0)
        self.assertIn(u'retiree', self.shal.about)
        self.assertIsNone(self.mona.about)

    def testReviews(self):
        self.assertIsInstance(self.shal.reviews, dict)
        self.assertEqual(len(self.shal.reviews), 0)

        # not using smooched as test because (s)he delete all the review
        self.assertIsInstance(self.smooched.reviews, dict)
        self.assertGreaterEqual(len(self.smooched.reviews), 0)
        '''
        self.assertIn(self.sao, self.smooched.reviews)
        self.assertIsInstance(self.smooched.reviews[self.sao][u'date'], datetime.date)
        self.assertEqual(self.smooched.reviews[self.sao][u'date'], datetime.date(year=2012, month=7, day=24))
        self.assertGreaterEqual(self.smooched.reviews[self.sao][u'people_helped'], 259)
        self.assertGreaterEqual(self.smooched.reviews[self.sao][u'people_total'], 644)
        self.assertEqual(self.smooched.reviews[self.sao][u'media_consumed'], 13)
        self.assertEqual(self.smooched.reviews[self.sao][u'media_total'], 25)
        self.assertEqual(self.smooched.reviews[self.sao][u'rating'], 6)
        self.assertIsInstance(self.smooched.reviews[self.sao][u'text'], unicode)
        self.assertGreater(len(self.smooched.reviews[self.sao][u'text']), 0)
        '''

        self.assertIsInstance(self.archaeon.reviews, dict)
        self.assertGreaterEqual(len(self.archaeon.reviews), 0)
        self.assertIn(self.fate_zero, self.archaeon.reviews)
        self.assertIsInstance(self.archaeon.reviews[self.fate_zero][u'date'], datetime.datetime)
        self.assertEqual(self.archaeon.reviews[self.fate_zero][u'date'],
                         datetime.datetime(year=2012, month=1, day=14, hour=8, minute=0))
        self.assertGreaterEqual(self.archaeon.reviews[self.fate_zero][u'people_helped'], 689)
        self.assertGreaterEqual(self.archaeon.reviews[self.fate_zero][u'people_total'], None)
        self.assertEqual(self.archaeon.reviews[self.fate_zero][u'media_consumed'], 13)
        self.assertEqual(self.archaeon.reviews[self.fate_zero][u'media_total'], 13)
        self.assertEqual(self.archaeon.reviews[self.fate_zero][u'rating'], 9)
        self.assertIsInstance(self.archaeon.reviews[self.fate_zero][u'text'], unicode)
        self.assertGreater(len(self.archaeon.reviews[self.fate_zero][u'text']), 0)

        self.assertIsInstance(self.threger.reviews, dict)
        self.assertEqual(len(self.threger.reviews), 0)

    def testRecommendations(self):
        self.assertIsInstance(self.shal.recommendations, dict)
        self.assertGreater(len(self.shal.recommendations), 0)
        self.assertIn(self.kanon, self.shal.recommendations)
        self.assertEqual(self.shal.recommendations[self.kanon][u'anime'], self.clannad_as)
        self.assertIsInstance(self.shal.recommendations[self.kanon][u'date'], datetime.date)
        self.assertEqual(self.shal.recommendations[self.kanon][u'date'],
                         datetime.datetime(year=2009, month=3, day=13, hour=5, minute=37))
        self.assertIsInstance(self.shal.recommendations[self.kanon][u'text'], unicode)
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
        self.assertIsInstance(self.shal.friends[self.ziron][u'last_active'], datetime.datetime)
        self.assertIn(self.ziron, self.shal.friends)
        self.assertIsInstance(self.shal.friends[self.ziron][u'last_active'], datetime.datetime)
        self.assertIn(self.seraph, self.shal.friends)
        self.assertIsInstance(self.shal.friends[self.seraph][u'last_active'], datetime.datetime)
        self.assertEqual(self.shal.friends[self.seraph][u'since'],
                         datetime.datetime(year=2012, month=10, day=13, hour=19, minute=31, second=0))
        self.assertIsInstance(self.mona.friends, dict)
        self.assertGreaterEqual(len(self.mona.friends), 0)
        self.assertIsInstance(self.threger.friends, dict)
        self.assertEqual(len(self.threger.friends), 0)
