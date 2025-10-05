import json
from datetime import datetime
from typing import Callable, Dict, Awaitable
from  app.core.logger import get_logger
from  app.core.event_bus import event_bus
from app.domain.heart_rate.events import HeartRateDataReceived

logger = get_logger("mqtt_gateway.handler", event_type="mqtt")

class MqttMessageRouter:
    def __init__(self):
        self._routes: Dict[str, Callable[[dict], Awaitable[None]]] = {}

    def register(self, topic: str, handler: Callable[[dict], Awaitable[None]]):
        self._routes[topic] = handler

    async def handle(self, topic: str, payload: bytes):
        try:
            data = json.loads(payload.decode())
            if topic in self._routes:
                await self._routes[topic](data)
            else:
                logger.warning(f"Unhandled topic: {topic}")
        except Exception as e:
            logger.error(f"Failed to handle MQTT message: {e}")

router = MqttMessageRouter()

# 注册心率事件
async def handle_heart_rate(data: dict):
    event = HeartRateDataReceived(
        patient_id=data["patient_id"],
        device_id=data["device_id"],
        value=int(data["value"]),
        timestamp=datetime.fromisoformat(data["timestamp"])
    )
    await event_bus.publish(HeartRateDataReceived, event)
    logger.info(f"Published HeartRateDataReceived: {event}")

router.register("health/heart_rate", handle_heart_rate)