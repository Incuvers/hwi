# -*- coding: utf-8 -*-
"""
Incuvers IRIS Hardware Interface
================================
Modified: 2021-10

Copyright © 2021 Incuvers. All rights reserved.
"""

import sys
import time
import os
import logging
import logging.config
import coloredlogs
from pathlib import Path
from envyaml import EnvYAML
from configparser import ConfigParser
from hwi.icb.encoder import RotaryEncoder

from hwi.logs.formatter import pformat
from hwi.amqp.client import AMQPClient
from hwi.alink.sensors import Sensors


def logging_handler(config_path: Path, base_path: str) -> None:
    """
    Configure monitor logger using dict config and set the logging path
    :param config_path: path to log config
    :type config_path: Path
    :param base_path: logging path
    :type base_path: str
    """
    os.makedirs(base_path, mode=0o777, exist_ok=True)
    # using split '.' to remove logs for rolling file handlers with format: <name>.log.<number>
    logs = list(
        filter(
            lambda file: 'log' in file.split('.'),
            os.listdir(path=base_path)
        )
    )
    # purge old logs on new instance
    for log in logs: os.remove(base_path + '/' + log)
    # bind logging to config file
    # verify path existance before initializing logger file configuration
    try:
        # load config from .yaml
        env = EnvYAML(config_path).export()
        logging.info("Parsed logger config:%s", pformat(env))
        logging.config.dictConfig(env)  # type: ignore
        logging.info('Configuring logger using dict config')
    except ValueError as exc:
        logging.exception(
            "Logging configuration failed due to missing environment variables: %s", exc)
    except FileNotFoundError:
        logging.exception(
            "Logging config file not found in expected absolute path: {}".format(config_path))
    else:
        logging.info("Logging configuration successful.")


def device_certs_handler(base_path: str) -> None:
    """
    Read device certs and export as environment variables for global access. 
    If device certs are missing exit with error code 2

    :param base_path: device certs base path
    :type base_path: str
    """
    if not os.path.exists(base_path + '/amqp.ini'):
        logging.critical("Failed to identify device certs.")
        sys.exit(2)
    # instantiate
    config = ConfigParser()
    config.read(base_path + '/amqp.ini')
    os.environ['AMQP_USER'] = config.get('amqp', 'user')
    os.environ['AMQP_PASS'] = config.get('amqp', 'password')


_log = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=_log)
_log.info("HWI Logs: %s", os.environ.get("HWI_LOGS"))
_log.info("HWI Certs: %s", os.environ.get("HWI_CERTS"))

logging_handler(
    config_path=Path(__file__).parent.joinpath("logs/config/config.yaml"),
    base_path=os.environ.get("HWI_LOGS", str(Path(__file__).parent.joinpath('logs/')))
)
device_certs_handler(
    base_path=os.environ.get("HWI_CERTS", str(
        Path(__file__).parent.parent.joinpath('instance/certs')))
)

# RMQ Event config
host = os.environ['RABBITMQ_ADDR'].split(':')[0]
port = int(os.environ['RABBITMQ_ADDR'].split(':')[1])
RotaryEncoder()
_log.info("Bound rotary encoder")
client = AMQPClient(host, port, os.environ.get('AMQP_USER', ''), os.environ.get('AMQP_PASS', ''))
time.sleep(5)
client.connect()
alink = Sensors(serial_port=os.environ.get('HWI_GPIO_SERIAL', '/dev/ttyS0'))
time.sleep(5)
alink.monitor()
