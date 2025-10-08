from app.adapters.pg_repository.device_repo import DeviceRepository
from app.domain.device.models import Device
from app.domain.device.events import DeviceCreated, DeviceUpdated, DeviceDeleted
from app.core.event_bus import event_bus
from datetime import datetime, timezone
from typing import List, Optional

class DeviceService:
    """
    设备服务层，处理设备相关业务逻辑。
    """

    def __init__(self, repo: DeviceRepository):
        self.repo = repo

    async def create_device(self, device: Device) -> int:
        """
        创建设备。
        参数:
            device: Device对象，name/serial_number 必填。
        返回:
            新增设备ID。
        异常:
            ValueError: 参数校验失败。
        """
        # 参数校验
        if not device.name or not device.serial_number:
            from app.core.logger import logger
            logger.error("设备创建失败：name和serial_number为必填项", extra={"event_type": "device_create"})
            raise ValueError("name和serial_number为必填项")
        # 唯一性校验
        exist = await self.repo.get_by_serial_number(device.serial_number)
        if exist:
            from app.core.logger import logger
            logger.error(f"设备创建失败：serial_number已存在({device.serial_number})", extra={"event_type": "device_create"})
            raise ValueError("serial_number已存在")
        device_id = await self.repo.create(device)
        event = DeviceCreated(
            id=device_id,
            name=device.name,
            type=device.type,
            serial_number=device.serial_number,
            manufacturer=device.manufacturer,
            model=device.model,
            note=device.note,
            created_at=datetime.now(timezone.utc),
        )
        await event_bus.publish(DeviceCreated.__name__, event)
        from app.core.logger import logger
        logger.info(f"设备创建成功，ID={device_id}", extra={"event_type": "device_create"})
        return device_id

    async def get_device(self, device_id: int) -> Optional[Device]:
        """
        获取设备信息。
        参数:
            device_id: 设备ID。
        返回:
            设备对象或None。
        """
        return await self.repo.get(device_id)

    async def update_device(self, device_id: int, device: Device) -> bool:
        """
        更新设备信息。
        参数:
            device_id: 设备ID。
            device: 新的设备对象。
        返回:
            是否更新成功。
        异常:
            ValueError: serial_number唯一性校验失败。
        """
        # serial_number唯一性校验
        if device.serial_number:
            exist = await self.repo.get_by_serial_number(device.serial_number)
            if exist and exist.id != device_id:
                from app.core.logger import logger
                logger.error(f"设备更新失败：serial_number已存在({device.serial_number})", extra={"event_type": "device_update"})
                raise ValueError("serial_number已存在")
        updated = await self.repo.update(device_id, device)
        if updated:
            event = DeviceUpdated(
                id=device_id,
                name=device.name,
                type=device.type,
                serial_number=device.serial_number,
                manufacturer=device.manufacturer,
                model=device.model,
                note=device.note,
                updated_at=datetime.now(timezone.utc),
            )
            await event_bus.publish(DeviceUpdated.__name__, event)
            from app.core.logger import logger
            logger.info(f"设备更新成功，ID={device_id}", extra={"event_type": "device_update"})
        else:
            from app.core.logger import logger
            logger.warning(f"设备更新失败，ID={device_id}未找到", extra={"event_type": "device_update"})
        return updated

    async def delete_device(self, device_id: int) -> bool:
        """
        删除设备。
        参数:
            device_id: 设备ID。
        返回:
            是否删除成功。
        """
        deleted = await self.repo.delete(device_id)
        from app.core.logger import logger
        if deleted:
            event = DeviceDeleted(
                id=device_id,
                deleted_at=datetime.now(timezone.utc),
            )
            await event_bus.publish(DeviceDeleted.__name__, event)
            logger.info(f"设备删除成功，ID={device_id}", extra={"event_type": "device_delete"})
        else:
            logger.warning(f"设备删除失败，ID={device_id}未找到", extra={"event_type": "device_delete"})
        return deleted

    async def list_devices(self, limit: int = 100, offset: int = 0) -> List[Device]:
        """
        获取设备列表。
        参数:
            limit: 返回数量上限。
            offset: 偏移量。
        返回:
            设备对象列表。
        """
        return await self.repo.list(limit=limit, offset=offset)