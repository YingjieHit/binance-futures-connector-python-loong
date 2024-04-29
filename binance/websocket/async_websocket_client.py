import json
import logging
from binance.lib.utils import get_timestamp  # Assuming this function exists in utils
from binance.websocket.async_binance_socket_manager import AsyncBinanceSocketManager


class AsyncWebsocketClient:
    ACTION_SUBSCRIBE = "SUBSCRIBE"
    ACTION_UNSUBSCRIBE = "UNSUBSCRIBE"

    def __init__(self,
                 stream_url,
                 on_message=None,
                 on_open=None,
                 on_close=None,
                 on_error=None,
                 on_ping=None,
                 on_pong=None,
                 proxies=None,
                 ):
        self.logger = logging.getLogger(__name__)
        self.socket_manager = AsyncBinanceSocketManager(
            stream_url,
            on_message=on_message if on_message else self.handle_message,
            on_open=on_open if on_open else self.on_open,
            on_close=on_close if on_close else self.on_close,
            on_error=on_error if on_error else self.on_error,
            on_ping=on_ping if on_ping else self.on_ping,
            on_pong=on_pong if on_pong else self.on_pong,
            proxies=proxies,
        )

    async def on_open(self):
        self.logger.info("WebSocket connection opened.")

    async def on_close(self):
        self.logger.info("WebSocket connection closed.")

    async def on_error(self, error):
        self.logger.error(f"An error occurred: {error}")

    async def on_ping(self):
        self.logger.info("WebSocket on ping.")

    async def on_pong(self):
        self.logger.info("WebSocket on pong.")

    async def handle_message(self, message):
        # Process the incoming message
        data = json.loads(message)
        self.logger.info(f"Received message: {data}")

    async def send_message_to_server(self, message, action=None, id=None):
        if not id:
            id = get_timestamp()
        if action != self.ACTION_UNSUBSCRIBE:
            return await self.subscribe(message, id=id)
        return await self.unsubscribe(message, id=id)

    async def subscribe(self, stream, id=None):
        print("执行订阅行情")
        if not id:
            id = get_timestamp()
        stream = [stream] if isinstance(stream, str) else stream
        json_msg = json.dumps({"method": "SUBSCRIBE", "params": stream, "id": id})
        await self.socket_manager.send_message(json_msg)
        print(f"Sent subscribe message for {stream}")

    async def unsubscribe(self, stream, id=None):
        if not id:
            id = get_timestamp()
        stream = [stream] if isinstance(stream, str) else stream
        json_msg = json.dumps({"method": "UNSUBSCRIBE", "params": stream, "id": id})
        await self.socket_manager.send_message(json_msg)
        print(f"Sent unsubscribe message for {stream}")

    async def ping(self):
        await self.socket_manager.ping()

    async def stop(self):
        await self.socket_manager.close()

    async def start(self):
        await self.socket_manager.run()

