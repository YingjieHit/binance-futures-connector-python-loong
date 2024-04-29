import asyncio
import websockets
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
        self.ws = None
        self.read_data_task = None

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
        self.read_data_task = asyncio.create_task(self.read_data())

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
