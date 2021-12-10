# -*- coding: utf-8 -*-
"""
HWI Init
========
Modified: 2021-10

Copyright © 2021 Incuvers. All rights reserved.
"""

import logging
import logging.config

from hwi.__version__ import __version__

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s"
)
logging.info("Incuvers™ Hardware Interface Version: %s", __version__)
