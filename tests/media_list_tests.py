#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import *
import os

if "RUNENV" in os.environ and os.environ["RUNENV"] == "travis":
    from myanimelist import session
    from myanimelist import media_list
    import myanimelist
else:
    from ..myanimelist import session
    from ..myanimelist import media_list
    from .. import myanimelist


class testMediaListClass(object):
    @classmethod
    def setUpClass(self):
        self.session = myanimelist.session.Session()

    @raises(TypeError)
    def testCannotInstantiateMediaList(self):
        myanimelist.media_list.MediaList(self.session, "test_username")
