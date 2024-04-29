#!/usr/bin/env python

import asyncio
import logging
from binance.lib.utils import config_logging
from binance.websocket.um_futures.async_websocket_client import AsyncUMFuturesWebsocketClient

config_logging(logging, logging.INFO)


# async def message_handler(_, message):
async def message_handler(message):
    print(message)


async def main():
    my_client = AsyncUMFuturesWebsocketClient(on_message=message_handler)
    await my_client.start()

    await my_client.book_ticker(symbol="btcusdt")

    await asyncio.sleep(100)

    logging.debug("closing ws connection")
    await my_client.stop()


if __name__ == '__main__':
    asyncio.run(main())
