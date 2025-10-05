from app.adapters.pg_repository.patient_device_repo import PatientDeviceRepository
from app.domain.patient_device.models import PatientDevice
from app.domain.patient_device.events import PatientDeviceBound, PatientDeviceUnbound
from app.core.event_bus import event_bus
from datetime import datetime
from typing import List, Optional

from app.adapters.pg_repository.device_repo import DeviceRepository
from app.adapters.pg_repository.patient_repo import PatientRepository
from app.core.logger import get_logger

class PatientDeviceService:
    """
    患者设备绑定服务，包含绑定、解绑等操作。
    """

    def __init__(self, repo: PatientDeviceRepository):
        self.repo = repo
        self.logger = get_logger("patient_device_service")

    async def bind_device(self, pd: PatientDevice) -> int:
        """
        绑定设备到患者。
        Args:
            pd (PatientDevice): 绑定关系对象，需包含 patient_id, device_id。
        Returns:
            int: 新增绑定关系ID。
        Raises:
            ValueError: 参数校验失败或唯一性冲突。
            Exception: 其他异常。
        """
        try:
            # 参数校验
            if not pd.patient_id or not pd.device_id:
                raise ValueError("patient_id 和 device_id 必填")
            # 检查患者是否存在
            patient_repo = PatientRepository(self.repo.client)
            patient = await patient_repo.get(pd.patient_id)
            if not patient:
                raise ValueError(f"患者不存在: {pd.patient_id}")
            # 检查设备是否存在
            device_repo = DeviceRepository(self.repo.client)
            device = await device_repo.get(pd.device_id)
            if not device:
                raise ValueError(f"设备不存在: {pd.device_id}")
            # 检查唯一性（同一患者同一设备未解绑不能重复绑定）
            existing = await self.repo.find_active_binding(pd.patient_id, pd.device_id)
            if existing:
                raise ValueError("该患者与设备已绑定，不能重复绑定")
            pd.bind_time = datetime.utcnow().isoformat()
            pd.unbind_time = None
            pd_id = await self.repo.create(pd)
            event = PatientDeviceBound(
                id=pd_id,
                patient_id=pd.patient_id,
                device_id=pd.device_id,
                bind_time=datetime.utcnow(),
            )
            await event_bus.publish(PatientDeviceBound.__name__, event)
            self.logger.info(f"患者设备绑定成功: {pd_id}")
            return pd_id
        except Exception as e:
            self.logger.error(f"患者设备绑定失败: {e}")
            raise

    async def unbind_device(self, pd_id: int) -> bool:
        """
        解绑患者设备关系。
        Args:
            pd_id (int): 绑定关系ID。
        Returns:
            bool: 是否解绑成功（幂等，已解绑也返回True）。
        """
        try:
            pd = await self.repo.get(pd_id)
            if not pd:
                self.logger.warning(f"解绑失败，记录不存在: {pd_id}")
                return False
            if pd.unbind_time:
                self.logger.info(f"解绑幂等处理，已解绑: {pd_id}")
                return True
            pd.unbind_time = datetime.utcnow().isoformat()
            updated = await self.repo.update(pd_id, pd)
            if updated:
                event = PatientDeviceUnbound(
                    id=pd_id,
                    patient_id=pd.patient_id,
                    device_id=pd.device_id,
                    unbind_time=datetime.utcnow(),
                )
                await event_bus.publish(PatientDeviceUnbound.__name__, event)
                self.logger.info(f"解绑成功: {pd_id}")
            else:
                self.logger.warning(f"解绑失败，更新未生效: {pd_id}")
            return updated
        except Exception as e:
            self.logger.error(f"解绑异常: {e}")
            raise

    async def get(self, pd_id: int) -> Optional[PatientDevice]:
        """
        获取绑定关系详情。
        Args:
            pd_id (int): 绑定关系ID。
        Returns:
            Optional[PatientDevice]: 绑定关系对象或None。
        """
        return await self.repo.get(pd_id)

    async def delete(self, pd_id: int) -> bool:
        """
        删除绑定关系（物理删除）。
        Args:
            pd_id (int): 绑定关系ID。
        Returns:
            bool: 是否删除成功。
        """
        return await self.repo.delete(pd_id)

    async def list(self, limit: int = 100, offset: int = 0) -> List[PatientDevice]:
        """
        获取绑定关系列表。
        Args:
            limit (int): 返回数量上限。
            offset (int): 偏移量。
        Returns:
            List[PatientDevice]: 绑定关系列表。
        """
        return await self.repo.list(limit=limit, offset=offset)