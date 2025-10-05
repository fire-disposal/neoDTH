from app.adapters.pg_repository.pgsql_client import PgSQLClient
from app.domain.patient_device.models import PatientDevice
from typing import List, Optional

class PatientDeviceRepository:
    """
    患者设备绑定关系数据仓储。
    """

    def __init__(self, client: PgSQLClient):
        self.client = client

    async def ensure_table(self) -> None:
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS patient_device (
                    id SERIAL PRIMARY KEY,
                    patient_id INTEGER NOT NULL,
                    device_id INTEGER NOT NULL,
                    bind_time TIMESTAMP,
                    unbind_time TIMESTAMP,
                    note TEXT
                )
                """
            )

    async def find_active_binding(self, patient_id: int, device_id: int) -> Optional[PatientDevice]:
        """
        查找未解绑的绑定关系（唯一性校验用）。
        Args:
            patient_id (int): 患者ID
            device_id (int): 设备ID
        Returns:
            Optional[PatientDevice]: 未解绑的绑定关系或None
        """
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT * FROM patient_device
                WHERE patient_id = $1 AND device_id = $2 AND unbind_time IS NULL
                """,
                patient_id,
                device_id,
            )
            if row:
                return PatientDevice(**dict(row))
            return None

    async def create(self, pd: PatientDevice) -> int:
        """
        新增绑定关系。
        Args:
            pd (PatientDevice): 绑定关系对象。
        Returns:
            int: 新增ID。
        """
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO patient_device (patient_id, device_id, bind_time, unbind_time, note)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id
                """,
                pd.patient_id,
                pd.device_id,
                pd.bind_time,
                pd.unbind_time,
                pd.note,
            )
            return row["id"]

    async def get(self, pd_id: int) -> Optional[PatientDevice]:
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM patient_device WHERE id = $1", pd_id
            )
            if row:
                return PatientDevice(**dict(row))
            return None

    async def update(self, pd_id: int, pd: PatientDevice) -> bool:
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE patient_device
                SET patient_id=$1, device_id=$2, bind_time=$3, unbind_time=$4, note=$5
                WHERE id=$6
                """,
                pd.patient_id,
                pd.device_id,
                pd.bind_time,
                pd.unbind_time,
                pd.note,
                pd_id,
            )
            return result[-1] != "0"

    async def delete(self, pd_id: int) -> bool:
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM patient_device WHERE id = $1", pd_id
            )
            return result[-1] != "0"

    async def list(self, limit: int = 100, offset: int = 0) -> List[PatientDevice]:
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM patient_device ORDER BY id LIMIT $1 OFFSET $2", limit, offset
            )
            return [PatientDevice(**dict(row)) for row in rows]