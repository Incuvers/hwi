# -*- coding: utf-8 -*-
"""
Rabbit MQ Client
================
Modified: 2021-10
"""

import pika


class RMQClient:
    def __init__(self, host: str, port: int) -> None:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port
            )
        )
        self.channel = connection.channel()
