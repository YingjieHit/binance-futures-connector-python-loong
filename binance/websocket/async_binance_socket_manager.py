# import asyncio
# import logging
# from typing import Optional
# import websockets
# from websockets.exceptions import WebSocketException
#
# from binance.lib.utils import parse_proxies
#
#
# class AsyncBinanceSocketManager:
#     def __init__(
#         self,
#         stream_url,
#         on_message=None,
#         on_open=None,
#         on_close=None,
#         on_error=None,
#         on_ping=None,
#         on_pong=None,
#         logger=None,
#         proxies: Optional[dict] = None,
#     ):
#         if not logger:
#             logger = logging.getLogger(__name__)
#         self.logger = logger
#         self.stream_url = stream_url
#         self.on_message = on_message
#         self.on_open = on_open
#         self.on_close = on_close
#         self.on_ping = on_ping
#         self.on_pong = on_pong
#         self.on_error = on_error
#         self.proxies = proxies
#
#         self._proxy_params = parse_proxies(proxies) if proxies else {}
#
#     async def connect(self):
#         self.logger.debug(f"Connecting to WebSocket Server at: {self.stream_url}, proxies: {self.proxies}")
#         try:
#             self.ws = await websockets.connect(self.stream_url, **self._proxy_params)
#             self.logger.debug("WebSocket connection established")
#             if self.on_open:
#                 await self.on_open(self)
#             await self.read_data()
#         except Exception as e:
#             self.logger.error(f"WebSocket connection failed: {e}")
#             if self.on_error:
#                 await self.on_error(self, e)
#
#     async def send_message(self, message):
#         self.logger.debug(f"Sending message: {message}")
#         await self.ws.send(message)
#
#     async def ping(self):
#         await self.ws.ping()
#
#     async def read_data(self):
#         try:
#             async for message in self.ws:
#                 if self.on_message:
#                     await self.on_message(self, message)
#         except WebSocketException as e:
#             self.logger.error(f"WebSocket error: {e}")
#             if self.on_error:
#                 await self.on_error(self, e)
#         finally:
#             if self.on_close:
#                 await self.on_close(self)
#
#     async def close(self):
#         self.logger.debug("Closing WebSocket connection")
#         await self.ws.close()
#
# # 示例用法
# async def on_message(manager, message):
#     print(f"Received message: {message}")
#
# async def main():
#     manager = AsyncBinanceSocketManager(
#         'wss://stream.binance.com:9443/ws/bnbbtc@ticker',
#         on_message=on_message
#     )
#     await manager.connect()
#
# if __name__ == "__main__":
#     asyncio.run(main())












import asyncio
import websockets
import json
import logging
from typing import Optional

from binance.lib.utils import parse_proxies


class AsyncBinanceSocketManager:
    def __init__(
        self,
        stream_url,
        on_message=None,
        on_open=None,
        on_close=None,
        on_error=None,
        on_ping=None,
        on_pong=None,
        logger=None,
        proxies: Optional[dict] = None,
    ):
        if not logger:
            logger = logging.getLogger(__name__)
        self.logger = logger
        self.stream_url = stream_url
        self.on_message = on_message
        self.on_open = on_open
        self.on_close = on_close
        self.on_error = on_error
        self.on_ping = on_ping
        self.on_pong = on_pong
        self.proxies = proxies
        self._proxy_params = parse_proxies(proxies) if proxies else {}
        self.ws: None = None

    async def connect(self):
        self.logger.debug(
            f"Creating connection with WebSocket Server: {self.stream_url}, proxies: {self.proxies}"
        )
        self.ws = await websockets.connect(self.stream_url, **self._proxy_params)
        self.logger.debug(
            f"WebSocket connection has been established: {self.stream_url}, proxies: {self.proxies}"
        )
        if self.on_open:
            await self.on_open()

    async def run(self):
        await self.connect()
        await self.read_data()

    async def send_message(self, message):
        self.logger.debug("Sending message to Binance WebSocket Server: %s", message)
        await self.ws.send(message)

    async def ping(self):
        await self.ws.ping()

    async def read_data(self):
        try:
            while True:
                message = await self.ws.recv()
                if self.on_message:
                    await self.on_message(message)
        except websockets.exceptions.WebSocketException as e:
            if self.on_error:
                await self.on_error(e)
            if self.on_close:
                await self.on_close()

    async def close(self):
        await self.ws.close()
        if self.on_close:
            await self.on_close()




