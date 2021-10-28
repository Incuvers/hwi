# -*- coding: utf-8 -*-
"""
HWI Entry
=========
Modified: 2021-10
"""

import os
import logging
import coloredlogs

_log = logging.getLogger(__name__)

coloredlogs.install(level="DEBUG", logger=_log)

# RMQ Event config
host = os.environ['RABBITMQ_ADDR'].split(':')[0]
port = int(os.environ['RABBITMQ_ADDR'].split(':')[1])
