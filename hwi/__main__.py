# -*- coding: utf-8 -*-
"""
Incuvers IRIS Hardware Interface
================================
Modified: 2021-10

Copyright © 2021 Incuvers. All rights reserved.
"""

import os
import logging
import logging.config
import coloredlogs
from pathlib import Path
from envyaml import EnvYAML

from hwi.logs.formatter import pformat
from hwi.rmq.client import RMQClient


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
        logging.config.dictConfig(env)
        logging.info('Configuring logger using dict config')
    except ValueError as exc:
        logging.exception(
            "Logging configuration failed due to missing environment variables: %s", exc)
    except FileNotFoundError:
        logging.exception(
            "Logging config file not found in expected absolute path: {}".format(config_path))
    else:
        logging.info("Logging configuration successful.")


logging_handler(
    config_path=Path(__file__).parent.joinpath("logs/config/config.yml"),
    base_path=os.environ.get("HWI_LOGS", str(Path(__file__).parent.joinpath('logs/')))
)

_log = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=_log)

# RMQ Event config
host = os.environ['RABBITMQ_ADDR'].split(':')[0]
port = int(os.environ['RABBITMQ_ADDR'].split(':')[1])

rmq_client = RMQClient(host, port)
rmq_client.publish()
