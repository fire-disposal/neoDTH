from app.adapters.pg_repository.pgsql_client import PgSQLClient
from app.domain.alert.models import HealthAlertRecord
from typing import List, Optional

class HealthAlertRepository:
    def __init__(self, client: PgSQLClient):
        self.client = client

    async def ensure_table(self) -> None:
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS health_alert (
                    id SERIAL PRIMARY KEY,
                    patient_id VARCHAR(64) NOT NULL,
                    device_id VARCHAR(64),
                    alert_type VARCHAR(64) NOT NULL,
                    alert_level VARCHAR(32) NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    resolved BOOLEAN NOT NULL DEFAULT FALSE,
                    resolved_at TIMESTAMP,
                    extra JSONB
                )
                """
            )

    async def create(self, alert: HealthAlertRecord) -> int:
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO health_alert
                (patient_id, device_id, alert_type, alert_level, message, created_at, resolved, resolved_at, extra)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                RETURNING id
                """,
                alert.patient_id,
                alert.device_id,
                alert.alert_type,
                alert.alert_level,
                alert.message,
                alert.created_at,
                alert.resolved,
                alert.resolved_at,
                alert.extra,
            )
            return row["id"]

    async def get(self, alert_id: int) -> Optional[HealthAlertRecord]:
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM health_alert WHERE id = $1", alert_id
            )
            if row:
                return HealthAlertRecord(**dict(row))
            return None

    async def list(self, patient_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[HealthAlertRecord]:
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            if patient_id:
                rows = await conn.fetch(
                    "SELECT * FROM health_alert WHERE patient_id = $1 ORDER BY created_at DESC LIMIT $2 OFFSET $3",
                    patient_id, limit, offset
                )
            else:
                rows = await conn.fetch(
                    "SELECT * FROM health_alert ORDER BY created_at DESC LIMIT $1 OFFSET $2",
                    limit, offset
                )
            return [HealthAlertRecord(**dict(row)) for row in rows]