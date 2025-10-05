from app.core.event_bus import event_bus
from app.core.logger import get_logger
from app.domain.heart_rate.events import HeartRateHighAlert
from app.domain.temperature.events import TemperatureHighAlert
from app.domain.sleep.events import SleepQualityAlert
from typing import Dict, Any
from datetime import datetime

logger = get_logger("HealthCombiner", event_type="aggregator")

class HealthCombiner:
    """
    订阅心率、体温、睡眠等高警报事件，进行跨指标健康事件聚合。
    例如：发热伴心动过速、睡眠异常伴高体温等。
    """

    def __init__(self):
        # 简单内存事件缓存，实际可用 Redis/DB 优化
        self.recent_events: Dict[str, Dict[str, Any]] = {}

    async def start(self):
        logger.info("HealthCombiner 初始化，订阅健康警报事件")
        event_bus.subscribe(HeartRateHighAlert.__name__, self.on_heart_rate_alert)
        event_bus.subscribe(TemperatureHighAlert.__name__, self.on_temperature_alert)
        event_bus.subscribe(SleepQualityAlert.__name__, self.on_sleep_alert)
        logger.info("HealthCombiner 事件订阅完成")

    async def on_heart_rate_alert(self, event: HeartRateHighAlert):
        logger.info(f"收到心率高警报: {event}")
        self._cache_event("heart_rate", event)
        await self._try_combine(event.patient_id)

    async def on_temperature_alert(self, event: TemperatureHighAlert):
        logger.info(f"收到体温高警报: {event}")
        self._cache_event("temperature", event)
        await self._try_combine(event.patient_id)

    async def on_sleep_alert(self, event: SleepQualityAlert):
        logger.info(f"收到睡眠异常警报: {event}")
        self._cache_event("sleep", event)
        await self._try_combine(event.patient_id)

    def _cache_event(self, key: str, event: Any):
        pid = event.patient_id
        if pid not in self.recent_events:
            self.recent_events[pid] = {}
        self.recent_events[pid][key] = {
            "event": event,
            "timestamp": event.timestamp
        }

    async def _try_combine(self, patient_id: str):
        """
        简单规则：10分钟内同时出现心率高警报和体温高警报，触发复合健康事件
        """
        events = self.recent_events.get(patient_id, {})
        hr = events.get("heart_rate")
        temp = events.get("temperature")
        if hr and temp:
            # 判断时间窗口
            if abs((hr["timestamp"] - temp["timestamp"]).total_seconds()) < 600:
                logger.warning(f"复合健康事件: 发热伴心动过速 [patient_id={patient_id}]")
                # TODO: 发布自定义复合事件，如 FeverWithTachycardiaEvent
                # await event_bus.publish("FeverWithTachycardiaEvent", {...})
                # 清理缓存，避免重复报警
                del self.recent_events[patient_id]["heart_rate"]
                del self.recent_events[patient_id]["temperature"]