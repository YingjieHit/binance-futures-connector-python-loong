#!/usr/bin/env python

import asyncio
import json
import logging
import numpy as np
import pandas as pd
from binance.lib.utils import config_logging
from binance.websocket.um_futures.async_websocket_client import AsyncUMFuturesWebsocketClient

config_logging(logging, logging.INFO)
queue_T = asyncio.Queue(maxsize=100)
l = []
my_client: AsyncUMFuturesWebsocketClient|None = None


# async def message_handler(_, message):
async def message_handler(message):
    global queue_T
    global l
    # 注意，刚开始接收到的是 {'result': None, 'id': 1714482328065}
    message = json.loads(message)
    print(message)
    if message.get('e') == 'depthUpdate':
        ts_ms = message.get('T')
        print(pd.to_datetime(ts_ms, unit='ms'))
        l.append(ts_ms)
        if len(l) >= 100:
            t_array = np.array(l)
            diff = np.diff(t_array)
            print(f"diff {diff}")
            await my_client.stop()

    # print("")


async def main():
    global my_client
    my_client = AsyncUMFuturesWebsocketClient(on_message=message_handler)
    await my_client.start()

    await my_client.partial_book_depth(symbol="btcusdt", level=5, speed=100)
    # await my_client.diff_book_depth(symbol='btcusdt', speed=100)

    await asyncio.sleep(100)

    logging.debug("closing ws connection")
    await my_client.stop()


if __name__ == '__main__':
    asyncio.run(main())
