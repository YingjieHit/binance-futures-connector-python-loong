import asyncio
import json
import logging

from binance.websocket.async_websocket_client import AsyncWebsocketClient

# 设置日志，以便观察运行情况
logging.basicConfig(level=logging.INFO)

# 通用的WebSocket URL，可以用于发送订阅请求
TEST_WEBSOCKET_URL = "wss://stream.binance.com:9443/ws"


async def handle_message(msg):
    data = json.loads(msg)
    print(data)


async def test_websocket_subscribe():
    # 创建客户端实例
    client = AsyncWebsocketClient(stream_url=TEST_WEBSOCKET_URL,


                                  )

    # 定义消息处理函数，输出接收到的数据
    client.handle_message = lambda msg: print("Received message:", msg)

    # 启动客户端并连接
    await client.start()
    print("订阅行情")
    # 发送订阅请求
    await client.subscribe('bnbbtc@ticker')
    await client.subscribe('ethbtc@ticker')

    # 等待一些时间以接收消息
    await asyncio.sleep(10)  # 等待10秒以便接收一些消息

    # 取消订阅
    await client.unsubscribe('bnbbtc@ticker')
    await client.unsubscribe('ethbtc@ticker')

    # 停止客户端并关闭连接
    await client.stop()


# 运行测试
if __name__ == "__main__":
    asyncio.run(test_websocket_subscribe())
