from app.adapters.pg_repository.pgsql_client import PgSQLClient
from app.domain.device.models import Device
from typing import List, Optional

class DeviceRepository:
    """
    设备数据仓储，负责设备表的CRUD操作。
    """

    def __init__(self, client: PgSQLClient):
        self.client = client

    async def ensure_table(self) -> None:
        """
        确保设备表存在。
        """
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS device (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(128) NOT NULL,
                    type VARCHAR(64),
                    serial_number VARCHAR(128) UNIQUE,
                    manufacturer VARCHAR(128),
                    model VARCHAR(128),
                    note TEXT
                )
                """
            )

    async def create(self, device: Device) -> int:
        """
        新增设备。
        参数:
            device: Device对象。
        返回:
            新增设备ID。
        """
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO device (name, type, serial_number, manufacturer, model, note)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id
                """,
                device.name,
                device.type,
                device.serial_number,
                device.manufacturer,
                device.model,
                device.note,
            )
            return row["id"]

    async def get(self, device_id: int) -> Optional[Device]:
        """
        根据ID获取设备。
        参数:
            device_id: 设备ID。
        返回:
            设备对象或None。
        """
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM device WHERE id = $1", device_id
            )
            if row:
                return Device(**dict(row))
            return None

    async def update(self, device_id: int, device: Device) -> bool:
        """
        更新设备。
        参数:
            device_id: 设备ID。
            device: 新的设备对象。
        返回:
            是否更新成功。
        """
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE device
                SET name=$1, type=$2, serial_number=$3, manufacturer=$4, model=$5, note=$6
                WHERE id=$7
                """,
                device.name,
                device.type,
                device.serial_number,
                device.manufacturer,
                device.model,
                device.note,
                device_id,
            )
            return result[-1] != "0"

    async def delete(self, device_id: int) -> bool:
        """
        删除设备。
        参数:
            device_id: 设备ID。
        返回:
            是否删除成功。
        """
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM device WHERE id = $1", device_id
            )
            return result[-1] != "0"

    async def list(self, limit: int = 100, offset: int = 0) -> List[Device]:
        """
        获取设备列表。
        参数:
            limit: 返回数量上限。
            offset: 偏移量。
        返回:
            设备对象列表。
        """
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM device ORDER BY id LIMIT $1 OFFSET $2", limit, offset
            )
            return [Device(**dict(row)) for row in rows]

    async def get_by_serial_number(self, serial_number: str) -> Optional[Device]:
        """
        根据serial_number查找设备。
        参数:
            serial_number: 序列号。
        返回:
            设备对象或None。
        """
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM device WHERE serial_number = $1", serial_number
            )
            if row:
                return Device(**dict(row))
            return None