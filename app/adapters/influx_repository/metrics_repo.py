from app.adapters.influx_repository.influx_client import InfluxClient
from app.domain.health_metrics.heart_rate.events import HeartRateDataReceived
from app.domain.health_metrics.temperature.events import TemperatureDataReceived
from typing import Any

class MetricsRepo:
    def __init__(self, client: InfluxClient):
        self.client = client

    async def write_heart_rate(self, event: HeartRateDataReceived) -> None:
        influx = self.client.get_client()
        point = {
            "measurement": "heart_rate",
            "tags": {
                "patient_id": event.patient_id,
                "device_id": event.device_id,
            },
            "fields": {
                "value": event.value,
            },
            "time": event.timestamp.isoformat(),
        }
        write_api = influx.write_api()
        write_api.write(bucket="neoDTH", record=point)

    async def write_temperature(self, event: TemperatureDataReceived) -> None:
        influx = self.client.get_client()
        point = {
            "measurement": "temperature",
            "tags": {
                "patient_id": event.patient_id,
                "device_id": event.device_id,
            },
            "fields": {
                "value": event.value,
            },
            "time": event.timestamp.isoformat(),
        }
        write_api = influx.write_api()
        write_api.write(bucket="neoDTH", record=point)