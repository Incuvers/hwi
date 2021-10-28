# -*- coding: utf-8 -*-
"""
Rabbit MQ Client
================
Modified: 2021-10
"""

import pika
import json
import time
import logging


class RMQClient:
    def __init__(self, host: str, port: int) -> None:
        self._logger = logging.getLogger(__name__)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port
            )
        )
        self.channel = connection.channel()
        self.channel.queue_declare(queue='test')

    def publish(self):
        body = json.dumps({"msg": "hello world"})
        while True:
            self.channel.basic_publish(exchange='',
                                       routing_key='test',
                                       body=body)
            self._logger.info("Sent %s", body)
            time.sleep(1)
