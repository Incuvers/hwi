# -*- coding: utf-8 -*-
"""
ICB Pinouts
===========
Modified: 2021-11

Copyright © 2021 Incuvers. All rights reserved.
"""

from enum import IntEnum

ROT_ENC_TABLE = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0]


class ICBHardware(IntEnum):
    PUSH_PIN = 22
    CLK_PIN = 17
    DT_PIN = 27
