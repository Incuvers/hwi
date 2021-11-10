# -*- coding: utf-8 -*-
"""
Unittests for Resolutions
=========================
Date: 2021-07

Dependencies:
-------------
Copyright © 2021 Incuvers. All rights reserved.
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

import unittest
from tests.resources import microscope
from hwi.microscope.camera.properties.resolution import CMOSConfig


class TestResolutions(unittest.TestCase):

    def setUp(self):
        name = microscope.CMOS_CONFIG.get('name', "")
        resolution = microscope.CMOS_CONFIG.get('width', 0), microscope.CMOS_CONFIG.get('height', 0)
        framerate = microscope.CMOS_CONFIG.get('framerate', "1/2")
        self.resolution = CMOSConfig(name, resolution, framerate)

    def tearDown(self):
        del self.resolution

    def test_getsetattrs(self):
        self.resolution.setattrs(**microscope.CMOS_CONFIG)
        self.assertDictEqual(self.resolution.getattrs(), microscope.CMOS_CONFIG)

    def test_repr(self):
        self.assertEqual(type(self.resolution.__repr__()), str)

    def test_name(self):
        self.resolution.name = "Test"
        self.assertEqual(self.resolution.name, "Test")

    def test_framerate(self):
        self.resolution.framerate = "1/2"
        self.assertEqual(self.resolution.framerate, "1/2")

    def test_width(self):
        self.resolution.width = 0
        self.assertEqual(self.resolution.width, 0)

    def test_length(self):
        self.resolution.length = 0
        self.assertEqual(self.resolution.length, 0)
