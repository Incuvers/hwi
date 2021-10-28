#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flash Service
=============
Modified: 2021-05

Dependencies:
-------------
```
import logging
from pathlib import Path
from monitor.sys import kernel
from monitor.environment.context_manager import ContextManager
```
Copyright © 2021 Incuvers. All rights reserved.
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

import logging
from pathlib import Path
from monitor.sys import kernel
from monitor.environment.context_manager import ContextManager


class FlashService:

    def __init__(self):
        # bind logging to config file
        self._logger = logging.getLogger(__name__)
        with ContextManager() as context:
            self._firmware_file_path = Path(
                f"{context.get_env('SNAP')}/lib/firmware/Incuvers_Incubator.ino.hex")
        self._avrdude_conf_file = Path(__file__).parent.joinpath('avrdude.conf')
        self._logger.info("Instantiation successful.")

    def flash_device(self):
        """
        flash the device with the provided hex file provided in the constructor
        :return: status code generated by compile and flash process if the code is not 0 the flash 
        was not successful
        """
        cmd_string = f'avrdude -v -p atmega2560 -cwiring -C {self._avrdude_conf_file} -P /dev/ttyUSB0 -b 115200 -D -U\
            flash:w:{self._firmware_file_path}:i'
        try:
            kernel.os_cmd(cmd_string)

        except OSError as exc:
            self._logger.critical(
                "os command failed with message: %s and exit status: %s", exc.strerror, exc.errno)
            if Path.exists(self._firmware_file_path):
                raise OSError from exc
            else:
                raise FileNotFoundError from exc

        else:
            self._logger.info("Firmware flash successful.")
