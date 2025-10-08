from app.adapters.pg_repository.pgsql_client import PgSQLClient
from app.domain.health_metrics.temperature.events import TemperatureDataReceived
from typing import Any

class TemperatureRepo:
    def __init__(self, client: PgSQLClient):
        self.client = client

    async def write_event_log(self, event: TemperatureDataReceived) -> None:
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO temperature_event_log (patient_id, device_id, value, timestamp)
                VALUES ($1, $2, $3, $4)
                """,
                event.patient_id,
                event.device_id,
                event.value,
                event.timestamp,
            )

    async def ensure_channel(self) -> None:
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS temperature_event_log (
                    id SERIAL PRIMARY KEY,
                    patient_id VARCHAR(64),
                    device_id VARCHAR(64),
                    value FLOAT,
                    timestamp TIMESTAMP
                )
                """
            )