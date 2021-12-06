# -*- coding: utf-8 -*-
"""
RabbitMQ Client
===============
Modified: 2021-10
"""

import json
import logging
from typing import Any, Dict
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from hwi.logs.formatter import pformat
from hwi.amqp.conf import AMQPConf
from hwi.events.registry import Registry as events


class AMQPClient:
    def __init__(self, host: str, port: int, username:str, password:str) -> None:
        credentials = PlainCredentials(
            username=username,
            password=password,
            erase_on_connect=True
        )
        self.connection = BlockingConnection(
            ConnectionParameters(
                host=host,
                port=port,
                virtual_host='/',
                credentials=credentials
            )
        )
        events.amqp_publish.register(
            callback=self.publish,
            priority=1
        )
        self._logger = logging.getLogger(__name__)

    def __del__(self) -> None:
        self.connection.close()
        self._logger.info("AMQP connection closed.")

    def connect(self) -> None:
        self.channel = self.connection.channel()
        self._logger.info("AMQP connection established with broker")

    def publish(self, route: str, body: Dict[str, Any]) -> None:
        if not self.channel:
            raise ConnectionError
        route_key = f'{AMQPConf.EXCHANGE}.{route}'
        self._logger.info("Message payload to %s: %s", route_key, pformat(body))
        self.channel.basic_publish(
            exchange=AMQPConf.EXCHANGE,
            routing_key=route_key,
            body=json.dumps(body)
        )
