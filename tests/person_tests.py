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
        self.hk_char = self.session.character(22745)
        self.hk_anime = self.session.anime(22745)
        self.hk_role = 'Supporting'

    def testNoIDInvalidPerson(self):
        with self.assertRaises(TypeError):
            self.session.character()

    def testNegativeInvalidPerson(self):
        with self.assertRaises(myanimelist.person.InvalidPersonError):
            self.session.character(-1)

    def testFloatInvalidPerson(self):
        with self.assertRaises(myanimelist.person.InvalidPersonError):
            self.session.character(1.5)

    def testNonExistentPerson(self):
        with self.assertRaises(myanimelist.person.InvalidPersonError):
            self.invalid_character.load()

    def testPersonValid(self):
        self.assertIsInstance(self.hiroshi_kamiya, myanimelist.person.Person)

    def testName(self):
        self.assertEqual(self.hiroshi_kamiya.name, u'Hiroshi_Kamiya')

    def testVoiceRoles(self):
        voice_roles = self.hiroshi_kamiya.voice_acting_roles
        self.assertIsInstance(voice_roles, dict)
        self.assertGreater(len(self.hiroshi_kamiya), 0)
        self.assertIn(self.hk.anime, self.hiroshi_kamiya.voice_acting_roles)
        self.assertIn(self.hk_char, self.hiroshi_kamiya.voice_acting_roles[self.hk_anime])
        role = self.hiroshi_kamiya.voice_acting_roles[self.hk_anime][self.hk_char]
        self.assertEqual(role, self.hk_role)
