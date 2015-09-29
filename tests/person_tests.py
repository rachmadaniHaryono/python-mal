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

        # false id
        self.invalid_person = self.session.person(47103248710328947109247)

        # test voice role
        self.hk_name = u'Hiroshi Kamiya'
        self.hk_anime = self.session.anime(22745)  # Juli
        self.hk_char = self.session.character(80873)  # Brothers Conflict Special
        self.hk_role = 'Supporting'

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
            self.invalid_character.load()

    def testPersonValid(self):
        self.assertIsInstance(self.hiroshi_kamiya, myanimelist.person.Person)

    def testName(self):
        self.assertEqual(self.hiroshi_kamiya.name, self.hk_name)

    def testVoiceRoles(self):
        voice_roles = self.hiroshi_kamiya.voice_acting_roles
        self.assertIsInstance(voice_roles, dict)
        self.assertGreater(len(voice_roles), 0)
        self.assertIn(self.hk.anime, voice_roles)
        self.assertIn(self.hk_char, voice_roles[self.hk_anime])
        role = voice_roles[self.hk_anime][self.hk_char]
        self.assertEqual(role, self.hk_role)
