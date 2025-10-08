from app.domain.health_metrics.sleep.events import SleepDataReceived, SleepQualityAlert
from app.adapters.influx_repository.metrics_repo import MetricsRepo
from app.adapters.pg_repository.temperature_repo import TemperatureRepo  # 假设复用体温 repo 结构
from app.core.event_bus import event_bus
from app.core.logger import get_logger

logger = get_logger("SleepProcessor", event_type="sleep")

class SleepProcessor:
    def __init__(self, influx_repo: MetricsRepo, pg_repo: TemperatureRepo, quality_threshold: str = "poor"):
        self.influx_repo = influx_repo
        self.pg_repo = pg_repo
        self.quality_threshold = quality_threshold

    async def handle_data_received(self, event: SleepDataReceived):
        logger.info(f"处理睡眠数据: {event}")
        await self.influx_repo.write_sleep(event)
        await self.pg_repo.write_event_log(event)
        if event.sleep_quality and event.sleep_quality.lower() == self.quality_threshold:
            alert = SleepQualityAlert(
                patient_id=event.patient_id,
                device_id=event.device_id,
                duration_minutes=event.duration_minutes,
                sleep_quality=event.sleep_quality,
                timestamp=event.timestamp,
                threshold=self.quality_threshold
            )
            logger.warning(f"睡眠质量警报: {alert}")
            await event_bus.publish(SleepQualityAlert.__name__, alert)