# -*- coding: utf-8 -*-
"""
Incuvers IRIS Hardware Interface
================================
Modified: 2021-10

Copyright © 2021 Incuvers. All rights reserved.
"""

import sys
import os
from threading import Thread
import time
import random
import json
import logging
import logging.config
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4
from envyaml import EnvYAML
from configparser import ConfigParser
from hwi.logs.formatter import pformat
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from hwi.system import wfi
from hwi.models.icb import ICB


EXCHANGE = 'device'
global icb

def logging_handler(config_path: Path, base_path: str) -> None:
    """
    Configure monitor logger using dict config and set the logging path
    :param config_path: path to log config
    :type config_path: Path
    :param base_path: logging path
    :type base_path: str
    """
    # set default log level if undef
    if not os.environ.get('HWI_LOG_LEVEL'):
        os.environ['HWI_LOG_LEVEL'] = "INFO"
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

def publish(route: str, body: Dict[str, Any]) -> None:
    route_key = f'{EXCHANGE}.{route}'
    _log.info("Message payload to %s: %s", route_key, pformat(body))
    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=route_key,
        body=json.dumps(body)
    )

def digest_command(ch, method, properties, body: bytes) -> None:
    _log.info("ch: %s:%s | method: %s:%s | properties: %s:%s | body: %s:%s",
              ch, type(ch), method, type(method), properties, type(properties), body, type(body))
    payload = json.loads(body.decode('utf-8'))
    _log.info("Message payload: %s", pformat(payload))

logging_handler(
    config_path=Path(__file__).parent.joinpath("logs/config/config.yaml"),
    base_path=os.environ.get("HWI_LOGS", str(Path(__file__).parent.joinpath('logs/')))
)
device_certs_handler(
    base_path=os.environ.get("HWI_CERTS", str(
        Path(__file__).parent.parent.joinpath('instance/certs')))
)

_log = logging.getLogger(__name__)
_log.info("HWI Logs: %s", os.environ.get("HWI_LOGS"))
_log.info("HWI Certs: %s", os.environ.get("HWI_CERTS"))
host = os.environ['RABBITMQ_ADDR'].split(':')[0]
port = int(os.environ['RABBITMQ_ADDR'].split(':')[1])

# blocking function call awaiting broker service
wfi(host, port, 30)
connection = BlockingConnection(
    ConnectionParameters(
        host=host,
        port=port,
        virtual_host='/',
        credentials=PlainCredentials(
            os.environ.get('AMQP_USER', ''), 
            os.environ.get('AMQP_PASS', ''),
            erase_on_connect=True
        )
    )
)
channel = connection.channel()
# subscribe to AMQP topics
channel.basic_consume(
    queue='command',
    auto_ack=True,
    on_message_callback=digest_command
)
_log.info("AMQP topic subscription established with broker")
Thread(target=channel.start_consuming, args=(), daemon=True).start()
_log.info("AMQP consuming loopback started")

# set initial values
icb = ICB()
tc = random.uniform(ICB.OPERATING_TEMPERATURE[0], ICB.OPERATING_TEMPERATURE[1])
icb.deserialize(
    {
        'TC': tc,
        'CC': random.uniform(ICB.CP_RANGE[0], ICB.CP_RANGE[1]),
        'OC': random.uniform(ICB.OP_RANGE[0], ICB.OP_RANGE[1]),
        'RH': random.uniform(0.0, 100.0),
        'TP': random.uniform(ICB.TP_RANGE[0], ICB.TP_RANGE[1]),
        'CP': random.uniform(ICB.OPERATING_TEMPERATURE[0], ICB.OPERATING_TEMPERATURE[1]),
        'OP': random.uniform(ICB.OP_RANGE[0], ICB.OP_RANGE[1]),
        'TO': random.uniform(0.0, 5.0),
        'CT': ICB.calibration_time_to_iso(random.randint(int(time.time()), int(time.time()+1000))),
        'CTR': tc,
        'TM': random.randint(0,2),
        'FP': random.randint(0,100),
        'FC': random.randint(0, 5000),
        'HP': random.randint(0,100),
        'HC': random.randint(0,1),
        'CM': random.randint(0,2),
        'OM': random.randint(0,2),
        'IV': '8e67a53',
    }
)

# main telemetry event loop
while True:
    telemetry = ICB()
    tc = random.uniform(ICB.OPERATING_TEMPERATURE[0], ICB.OPERATING_TEMPERATURE[1])
    document = {
        'TC': tc,
        'CC': random.uniform(ICB.CP_RANGE[0], ICB.CP_RANGE[1]),
        'OC': random.uniform(ICB.OP_RANGE[0], ICB.OP_RANGE[1]),
        'RH': random.uniform(0.0, 100.0),
        'TP': icb.tp,
        'CP': icb.cp,
        'OP': icb.op,
        'TO': icb.to,
        'CT': icb.ct,
        'CTR': tc,
        'TM': icb.tm,
        'FP': icb.fp,
        'FC': random.randint(0, 5000),
        'HP': icb.hp,
        'HC': random.randint(0,1),
        'CM': icb.cm,
        'OM': icb.om,
        'IV': icb.iv,
    }
    telemetry.deserialize(document)
    publish('telemetry', telemetry.serialize())
    time.sleep(1)
