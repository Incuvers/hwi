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
from hwi.sys import system


class AMQPClient:
    def __init__(self, host: str, port: int, username:str, password:str) -> None:
        self._logger = logging.getLogger(__name__)
        events.amqp_publish.register(
            callback=self.publish,
            priority=1
        )
        # blocking function call awaiting broker service
        system.wfi(host, port, 30)
        self.connection = BlockingConnection(
            ConnectionParameters(
                host=host,
                port=port,
                virtual_host='/',
                credentials=PlainCredentials(username, password, erase_on_connect=True)
            )
        )
        self.channel = self.connection.channel()
        self._logger.info("%s instantiated successfully", __name__)

    def __del__(self) -> None:
        self.connection.close()
        self._logger.info("AMQP connection closed.")

    def publish(self, route: str, body: Dict[str, Any]) -> None:
        route_key = f'{AMQPConf.EXCHANGE}.{route}'
        self._logger.info("Message payload to %s: %s", route_key, pformat(body))
        self.channel.basic_publish(
            exchange=AMQPConf.EXCHANGE,
            routing_key=route_key,
            body=json.dumps(body)
        )
