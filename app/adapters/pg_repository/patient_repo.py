from app.adapters.pg_repository.pgsql_client import PgSQLClient
from app.domain.patient.models import Patient
from typing import List, Optional

from app.adapters.pg_repository.pgsql_client import PgSQLClient
from app.domain.patient.models import Patient
from typing import List, Optional
from app.core.logger import get_logger

logger = get_logger("patient_repo")

class PatientRepository:
    """
    患者数据仓储，负责与数据库交互。
    """
    def __init__(self, client: PgSQLClient):
        self.client = client

    async def ensure_table(self) -> None:
        """
        确保患者表存在。
        """
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS patient (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(128) NOT NULL,
                    gender VARCHAR(16),
                    birth_date DATE,
                    phone VARCHAR(32),
                    address VARCHAR(256),
                    note TEXT
                )
                """
            )

    async def create(self, patient: Patient) -> int:
        """
        新增患者记录。
        Args:
            patient (Patient): 患者对象
        Returns:
            int: 新增患者ID
        Raises:
            Exception: 数据库异常
        """
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            try:
                row = await conn.fetchrow(
                    """
                    INSERT INTO patient (name, gender, birth_date, phone, address, note)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING id
                    """,
                    patient.name,
                    patient.gender,
                    patient.birth_date,
                    patient.phone,
                    patient.address,
                    patient.note,
                )
                logger.info(f"患者新增成功: {row['id']}")
                return row["id"]
            except Exception as e:
                logger.error(f"患者新增失败: {e}")
                raise

    async def get(self, patient_id: int) -> Optional[Patient]:
        """
        获取患者信息。
        Args:
            patient_id (int): 患者ID
        Returns:
            Optional[Patient]: 患者对象或None
        """
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            try:
                row = await conn.fetchrow(
                    "SELECT * FROM patient WHERE id = $1", patient_id
                )
                if row:
                    logger.info(f"获取患者成功: {patient_id}")
                    return Patient(**dict(row))
                logger.warning(f"未找到患者: {patient_id}")
                return None
            except Exception as e:
                logger.error(f"获取患者失败: {e}")
                raise

    async def update(self, patient_id: int, patient: Patient) -> bool:
        """
        更新患者信息。
        Args:
            patient_id (int): 患者ID
            patient (Patient): 新患者数据
        Returns:
            bool: 是否更新成功
        """
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            try:
                result = await conn.execute(
                    """
                    UPDATE patient
                    SET name=$1, gender=$2, birth_date=$3, phone=$4, address=$5, note=$6
                    WHERE id=$7
                    """,
                    patient.name,
                    patient.gender,
                    patient.birth_date,
                    patient.phone,
                    patient.address,
                    patient.note,
                    patient_id,
                )
                success = result[-1] != "0"
                if success:
                    logger.info(f"患者更新成功: {patient_id}")
                else:
                    logger.warning(f"患者更新失败: {patient_id}")
                return success
            except Exception as e:
                logger.error(f"患者更新异常: {e}")
                raise

    async def delete(self, patient_id: int) -> bool:
        """
        删除患者信息。
        Args:
            patient_id (int): 患者ID
        Returns:
            bool: 是否删除成功
        """
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            try:
                result = await conn.execute(
                    "DELETE FROM patient WHERE id = $1", patient_id
                )
                success = result[-1] != "0"
                if success:
                    logger.info(f"患者删除成功: {patient_id}")
                else:
                    logger.warning(f"患者删除失败: {patient_id}")
                return success
            except Exception as e:
                logger.error(f"患者删除异常: {e}")
                raise

    async def list(self, limit: int = 100, offset: int = 0) -> List[Patient]:
        """
        分页获取患者列表。
        Args:
            limit (int): 每页数量
            offset (int): 偏移量
        Returns:
            List[Patient]: 患者列表
        """
        pool = await self.client.get_pool()
        async with pool.acquire() as conn:
            try:
                rows = await conn.fetch(
                    "SELECT * FROM patient ORDER BY id LIMIT $1 OFFSET $2", limit, offset
                )
                logger.info(f"获取患者列表: {len(rows)} 条")
                return [Patient(**dict(row)) for row in rows]
            except Exception as e:
                logger.error(f"获取患者列表失败: {e}")
                raise