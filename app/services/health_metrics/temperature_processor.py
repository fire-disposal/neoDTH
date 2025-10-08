from app.domain.health_metrics.temperature.events import TemperatureDataReceived, TemperatureHighAlert
from app.adapters.influx_repository.metrics_repo import MetricsRepo
from app.adapters.pg_repository.temperature_repo import TemperatureRepo
from app.core.event_bus import event_bus
from app.core.logger import get_logger

logger = get_logger("TemperatureProcessor", event_type="temperature")

class TemperatureProcessor:
    def __init__(self, influx_repo: MetricsRepo, pg_repo: TemperatureRepo, high_threshold: float = 38.0):
        self.influx_repo = influx_repo
        self.pg_repo = pg_repo
        self.high_threshold = high_threshold

    async def handle_data_received(self, event: TemperatureDataReceived):
        logger.info(f"处理体温数据: {event}")
        await self.influx_repo.write_temperature(event)
        await self.pg_repo.write_event_log(event)
        if event.value >= self.high_threshold:
            alert = TemperatureHighAlert(
                patient_id=event.patient_id,
                device_id=event.device_id,
                value=event.value,
                timestamp=event.timestamp,
                threshold=self.high_threshold
            )
            logger.warning(f"体温高警报: {alert}")
            await event_bus.publish(TemperatureHighAlert.__name__, alert)