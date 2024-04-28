#!/usr/bin/env python

import time
import json
import logging
from binance.lib.utils import config_logging
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

config_logging(logging, logging.DEBUG)


def message_handler(_, message: str):
    # print(message)
    message = json.loads(message)
    print(message['b'])
    print(len(message['b']))


my_client = UMFuturesWebsocketClient(on_message=message_handler)

my_client.partial_book_depth(
    symbol="bnbusdt",
    id=1,
    level=10,
    speed=100,
)

time.sleep(10)

logging.debug("closing ws connection")
my_client.stop()
