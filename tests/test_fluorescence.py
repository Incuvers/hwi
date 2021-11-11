# -*- coding: utf-8 -*-
"""
Fluorescence Unittests
======================
Modified: 2021-07

Dependencies:
-------------
```
import logging
import wiringpi
from monitor.microscope.fluorescence.hardware import FluorescenceHardware
```
Copyright © 2021 Incuvers. All rights reserved.
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

import time
import logging
import unittest
from unittest.mock import MagicMock, patch, Mock
from hwi.microscope.fluorescence.hardware import FluorescenceHardware
from hwi.microscope.fluorescence.fluorescence import Fluorescence


class TestFluorescence(unittest.TestCase):
    def setUp(self):
        self.wiring_pi = Mock()
        mocked_modules = {
            'wiringpi': self.wiring_pi
        }
        self.module_patcher = patch.dict('sys.modules', mocked_modules)
        self.module_patcher.start()
        logging.disable()
        self.fluo = Fluorescence()

    def tearDown(self):
        del self.fluo
        logging.disable(logging.NOTSET)

    def test_initialized(self):
        """
        Test fluorescence hardware initialization
        """
        self.fluo.initialize_hardware()
        self.wiring_pi.wiringPiSetupGpio.assert_called_once()
        self.wiring_pi.pinMode.assert_called_once_with(
            FluorescenceHardware.TRIGGER, self.wiring_pi.OUTPUT)
        self.assertTrue(self.fluo.initialized)

    @patch.object(time, 'sleep')
    @patch('monitor.microscope.fluorescence.fluorescence.Fluorescence.enable')
    @patch('monitor.microscope.fluorescence.fluorescence.Fluorescence.cooldown_timer')
    def test_watchdog_timer(self, cooldown_timer: MagicMock, enable: MagicMock, sleep: MagicMock):
        """
        Test watchdog event loop

        :param cooldown_timer: [description]
        :type cooldown_timer: MagicMock
        :param enable: [description]
        :type enable: MagicMock
        :param sleep: [description]
        :type sleep: MagicMock
        """
        # test early return
        self.fluo.state = False
        self.fluo.watchdog_timer()
        sleep.assert_not_called()
        # test burnout limit
        self.fluo.state = True
        self.fluo.watchdog_timer()
        enable.assert_called_once_with(False)
        cooldown_timer.assert_called_once()

    @patch.object(time, 'sleep')
    def test_cooldown_timer(self, sleep: MagicMock):
        """
        Test cooldown event loop

        :param sleep: [description]
        :type sleep: MagicMock
        """
        self.fluo.cooldown_timer()
        self.assertFalse(self.fluo.cooldown)

    @patch('monitor.microscope.fluorescence.fluorescence.Fluorescence.watchdog_timer')
    def test_enable(self, watchdog: MagicMock):
        """
        Test fled interface

        :param watchdog: [description]
        :type watchdog: MagicMock
        """
        # enable
        self.fluo.enable(True)
        watchdog.assert_called_once()
        watchdog.reset_mock()
        # disable
        self.fluo.enable(False)
        watchdog.assert_not_called()
