#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase

import myanimelist.session
import myanimelist.person
# import myanimelist.anime
# import myanimelist.character


class testPersonClass(TestCase):
    @classmethod
    def setUpClass(self):
        self.session = myanimelist.session.Session()
        self.hiroshi_kamiya = self.session.person(118)

        # test voice role
        self.hk_name = 'Hiroshi Kamiya'
        self.hk_anime = self.session.anime(15605)  # Brothers Conflict
        self.hk_char = self.session.character(80873)  # Juli
        self.hk_role = 'Supporting'
        self.hk_position = 'Theme Song Performance'
        # test no voice role person
        self.sawano = self.session.person(8509)  # sawano hiroyuki

        # test no position person
        self.nayeli = self.session.person(9872)  # nayeli forest

    def testNoIDInvalidPerson(self):
        with self.assertRaises(TypeError):
            self.session.person()

    def testNegativeInvalidPerson(self):
        with self.assertRaises(myanimelist.person.InvalidPersonError):
            self.session.person(-1)

    def testFloatInvalidPerson(self):
        with self.assertRaises(myanimelist.person.InvalidPersonError):
            self.session.person(1.5)

    def testNonExistentPerson(self):
        with self.assertRaises(myanimelist.person.InvalidPersonError):
            person_short = self.session.person(49732)  # for short int
            person_short.load()
        with self.assertRaises(myanimelist.person.InvalidPersonError):
            person_long = self.session.person(4973204723047)  # for long int
            person_long.load()

    def testPersonValid(self):
        self.assertIsInstance(self.hiroshi_kamiya, myanimelist.person.Person)

    def testName(self):
        self.assertEqual(self.hiroshi_kamiya.name, self.hk_name)

    def testVoiceRoles(self):
        voice_roles = self.hiroshi_kamiya.voice_acting_roles
        self.assertIsInstance(voice_roles, dict)
        self.assertGreater(len(voice_roles), 0)
        self.assertIn(self.hk_anime, voice_roles)
        self.assertIn(self.hk_char, voice_roles[self.hk_anime])
        role = voice_roles[self.hk_anime][self.hk_char]
        self.assertEqual(role, self.hk_role)

    def testNoVoiceRoles(self):
        voice_roles = self.sawano.voice_acting_roles
        self.assertIsNone(voice_roles)

    def testPersonPosition(self):
        """test person position."""
        hk_positions = self.hiroshi_kamiya.anime_staff_positions

        self.assertIsInstance(hk_positions, dict)
        self.assertGreater(len(hk_positions), 0)

        self.assertIn(self.hk_anime, hk_positions)
        self.assertIn(self.hk_position, hk_positions[self.hk_anime])
        self.assertIsInstance(hk_positions[self.hk_anime], list)
        self.assertGreater(len(hk_positions[self.hk_anime]), 0)

    def testNoPersonPosition(self):
        positions = self.nayeli.anime_staff_positions
        self.assertIsNone(positions)
