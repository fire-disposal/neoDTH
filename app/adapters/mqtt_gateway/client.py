import asyncio
import json
from aiomqtt import Client, MqttError
from typing import Callable, List, Optional
from  app.core.logger import get_logger

class AsyncMQTTClient:
    def __init__(
        self,
        broker_host: str,
        broker_port: int = 1883,
        topics: Optional[List[str]] = None,
        on_message: Optional[Callable[[str, bytes], None]] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        client_id: Optional[str] = None,
    ):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.topics = topics or []
        self.on_message = on_message
        self.username = username
        self.password = password
        self.client_id = client_id
        self.logger = get_logger("mqtt_gateway", event_type="mqtt")
        self._client = None
        self._running = False

    async def connect(self):
        self.logger.info("准备连接MQTT服务")
        try:
            self.logger.info(f"Connecting to MQTT broker {self.broker_host}:{self.broker_port}")
            self._client = Client(
                self.broker_host,
                self.broker_port,
                username=self.username,
                password=self.password,
                client_id=self.client_id,
            )
            await self._client.__aenter__()
            self._running = True
            self.logger.info("MQTT连接成功")
        except Exception as e:
            self.logger.error(f"MQTT连接异常: {e}")
            raise

    async def disconnect(self):
        self.logger.info("准备断开MQTT连接")
        if self._client:
            await self._client.__aexit__(None, None, None)
            self.logger.info("Disconnected from MQTT broker")
            self._running = False
        self.logger.info("MQTT连接已断开，资源已清理")

    async def subscribe(self, topics: Optional[List[str]] = None):
        topics = topics or self.topics
        for topic in topics:
            await self._client.subscribe(topic)
            self.logger.info(f"Subscribed to topic: {topic}")

    async def listen(self):
        if not self._client:
            raise RuntimeError("MQTT client not connected")
        async with self._client.unfiltered_messages() as messages:
            await self.subscribe()
            self.logger.info("Start listening for MQTT messages")
            async for message in messages:
                try:
                    if self.on_message:
                        await self.on_message(message.topic, message.payload)
                except Exception as e:
                    self.logger.error(f"Error in message handler: {e}")

    async def run_forever(self):
        self.logger.info("MQTT客户端进入run_forever主循环")
        while True:
            try:
                await self.connect()
                await self.listen()
            except MqttError as e:
                self.logger.error(f"MQTT error: {e}, reconnecting in 5s...")
                await asyncio.sleep(5)
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}, reconnecting in 5s...")
                await asyncio.sleep(5)
            finally:
                await self.disconnect()