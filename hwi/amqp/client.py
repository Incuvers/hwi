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
    def __init__(self, host: str, port: int) -> None:
        self.connection = None
        self.channel = None
        self.host = host
        self.port = port
        events.amqp_publish.register(
            callback=self.publish,
            priority=1
        )
        self._logger = logging.getLogger(__name__)

    def connect(self) -> None:
        self._logger.debug("Creating rabbitmq connection to host: %s port: %s",
                           self.host, self.port)
        credentials = PlainCredentials(
            username="microservice",
            password="microservice",
            erase_on_connect=True
        )
        self.connection = BlockingConnection(
            ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host='/',
                credentials=credentials
            )
        )
        self.channel = self.connection.channel()
        self._logger.info("AMQP connection established with broker %s:%s", self.host, self.port)

    def publish(self, route: str, body: Dict[str, Any]) -> None:
        if not self.channel:
            raise ConnectionError
        route_key = f'{AMQPConf.EXCHANGE}.{route}'
        self._logger.info("Message payload to %s: %s", route_key, pformat(body))
        self.channel.basic_publish(exchange=AMQPConf.EXCHANGE,
                                   routing_key=route_key,
                                   body=json.dumps(body))
