from app.adapters.pg_repository.patient_repo import PatientRepository
from app.domain.patient.models import Patient
from app.domain.patient.events import PatientCreated, PatientUpdated, PatientDeleted
from app.core.event_bus import event_bus
from datetime import datetime
from typing import List, Optional

from app.adapters.pg_repository.patient_repo import PatientRepository
from app.domain.patient.models import Patient
from app.domain.patient.events import PatientCreated, PatientUpdated, PatientDeleted
from app.core.event_bus import event_bus
from datetime import datetime
from typing import List, Optional
from app.core.logger import get_logger

logger = get_logger("patient_service")

class PatientService:
    """
    患者服务层，处理业务逻辑。
    """
    def __init__(self, repo: PatientRepository):
        self.repo = repo

    async def create_patient(self, patient: Patient) -> int:
        """
        创建患者。
        Args:
            patient (Patient): 患者对象
        Returns:
            int: 新增患者ID
        Raises:
            ValueError: 参数校验失败
            Exception: 数据库异常
        """
        try:
            # 额外参数校验（如有）
            if not patient.name or not patient.name.strip():
                raise ValueError("姓名不能为空")
            patient_id = await self.repo.create(patient)
            event = PatientCreated(
                id=patient_id,
                name=patient.name,
                gender=patient.gender,
                birth_date=str(patient.birth_date) if patient.birth_date else None,
                phone=patient.phone,
                address=patient.address,
                note=patient.note,
                created_at=datetime.utcnow(),
            )
            await event_bus.publish(PatientCreated.__name__, event)
            logger.info(f"创建患者成功: {patient_id}")
            return patient_id
        except Exception as e:
            logger.error(f"创建患者失败: {e}")
            raise

    async def get_patient(self, patient_id: int) -> Optional[Patient]:
        """
        获取患者信息。
        Args:
            patient_id (int): 患者ID
        Returns:
            Optional[Patient]: 患者对象或None
        """
        try:
            patient = await self.repo.get(patient_id)
            if patient:
                logger.info(f"获取患者成功: {patient_id}")
            else:
                logger.warning(f"未找到患者: {patient_id}")
            return patient
        except Exception as e:
            logger.error(f"获取患者失败: {e}")
            raise

    async def update_patient(self, patient_id: int, patient: Patient) -> bool:
        """
        更新患者信息。
        Args:
            patient_id (int): 患者ID
            patient (Patient): 新患者数据
        Returns:
            bool: 是否更新成功
        """
        try:
            if not patient.name or not patient.name.strip():
                raise ValueError("姓名不能为空")
            updated = await self.repo.update(patient_id, patient)
            if updated:
                event = PatientUpdated(
                    id=patient_id,
                    name=patient.name,
                    gender=patient.gender,
                    birth_date=str(patient.birth_date) if patient.birth_date else None,
                    phone=patient.phone,
                    address=patient.address,
                    note=patient.note,
                    updated_at=datetime.utcnow(),
                )
                await event_bus.publish(PatientUpdated.__name__, event)
                logger.info(f"更新患者成功: {patient_id}")
            else:
                logger.warning(f"更新患者失败: {patient_id}")
            return updated
        except Exception as e:
            logger.error(f"更新患者异常: {e}")
            raise

    async def delete_patient(self, patient_id: int) -> bool:
        """
        删除患者信息。
        Args:
            patient_id (int): 患者ID
        Returns:
            bool: 是否删除成功
        """
        try:
            deleted = await self.repo.delete(patient_id)
            if deleted:
                event = PatientDeleted(
                    id=patient_id,
                    deleted_at=datetime.utcnow(),
                )
                await event_bus.publish(PatientDeleted.__name__, event)
                logger.info(f"删除患者成功: {patient_id}")
            else:
                logger.warning(f"删除患者失败: {patient_id}")
            return deleted
        except Exception as e:
            logger.error(f"删除患者异常: {e}")
            raise

    async def list_patients(self, limit: int = 100, offset: int = 0) -> List[Patient]:
        """
        分页获取患者列表。
        Args:
            limit (int): 每页数量
            offset (int): 偏移量
        Returns:
            List[Patient]: 患者列表
        """
        try:
            result = await self.repo.list(limit=limit, offset=offset)
            logger.info(f"获取患者列表: {len(result)} 条")
            return result
        except Exception as e:
            logger.error(f"获取患者列表失败: {e}")
            raise