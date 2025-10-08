from app.domain.health_metrics.heart_rate.events import HeartRateDataReceived, HeartRateHighAlert
from app.adapters.influx_repository.metrics_repo import MetricsRepo
from app.adapters.pg_repository.heart_rate_repo import HeartRateRepo
from app.core.event_bus import event_bus
from app.core.logger import get_logger

logger = get_logger("HeartRateProcessor", event_type="heart_rate")

class HeartRateProcessor:
    def __init__(self, influx_repo: MetricsRepo, pg_repo: HeartRateRepo, high_threshold: int = 120):
        self.influx_repo = influx_repo
        self.pg_repo = pg_repo
        self.high_threshold = high_threshold

    async def handle_data_received(self, event: HeartRateDataReceived):
        logger.info(f"处理心率数据: {event}")
        await self.influx_repo.write_heart_rate(event)
        await self.pg_repo.write_event_log(event)
        if event.value >= self.high_threshold:
            alert = HeartRateHighAlert(
                patient_id=event.patient_id,
                device_id=event.device_id,
                value=event.value,
                timestamp=event.timestamp,
                threshold=self.high_threshold
            )
            logger.warning(f"心率高警报: {alert}")
            await event_bus.publish(HeartRateHighAlert.__name__, alert)