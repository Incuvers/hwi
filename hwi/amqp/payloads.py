# -*- coding: utf-8 -*-
"""
AMQP Payload Enums
==================
Modified: 2021-11

Copyright © 2021 Incuvers. All rights reserved.
"""

from enum import IntEnum


class ISR(IntEnum):

    PUSH = 0
    CW = 1
    CCW = 2
