from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.domain.device.models import Device
from app.services.device_service import DeviceService
from app.adapters.pg_repository.pgsql_client import PgSQLClient
from app.adapters.pg_repository.device_repo import DeviceRepository

router = APIRouter(prefix="/devices", tags=["devices"])

def get_service():
    """
    获取设备服务实例。
    权限控制预留：如需鉴权，可在此处注入用户信息或权限依赖。
    """
    client = PgSQLClient()
    repo = DeviceRepository(client)
    return DeviceService(repo)

@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def create_device(
    device: Device,
    service: DeviceService = Depends(get_service)
) -> int:
    """
    创建设备。
    参数:
        device: 设备对象，包含 name、serial_number 等字段，name/serial_number 必填。
    返回:
        新增设备的ID。
    """
    return await service.create_device(device)

@router.get("/{device_id}", response_model=Device)
async def get_device(
    device_id: int,
    service: DeviceService = Depends(get_service)
) -> Device:
    """
    获取指定ID的设备信息。
    参数:
        device_id: 设备ID。
    返回:
        设备对象。
    异常:
        404 - 未找到设备。
    """
    device = await service.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.put("/{device_id}", response_model=bool)
async def update_device(
    device_id: int,
    device: Device,
    service: DeviceService = Depends(get_service)
) -> bool:
    """
    更新指定ID的设备信息。
    参数:
        device_id: 设备ID。
        device: 新的设备对象。
    返回:
        是否更新成功。
    异常:
        404 - 未找到设备。
    """
    updated = await service.update_device(device_id, device)
    if not updated:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated

@router.delete("/{device_id}", response_model=bool)
async def delete_device(
    device_id: int,
    service: DeviceService = Depends(get_service)
) -> bool:
    """
    删除指定ID的设备。
    参数:
        device_id: 设备ID。
    返回:
        是否删除成功。
    异常:
        404 - 未找到设备。
    """
    deleted = await service.delete_device(device_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Device not found")
    return deleted

@router.get("/", response_model=List[Device])
async def list_devices(
    limit: int = 100,
    offset: int = 0,
    service: DeviceService = Depends(get_service)
) -> List[Device]:
    """
    获取设备列表。
    参数:
        limit: 返回数量上限，默认100。
        offset: 偏移量，默认0。
    返回:
        设备对象列表。
    """
    return await service.list_devices(limit=limit, offset=offset)