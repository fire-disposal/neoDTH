from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.domain.patient_device.models import PatientDevice
from app.services.patient_device_service import PatientDeviceService
from app.adapters.pg_repository.pgsql_client import PgSQLClient
from app.adapters.pg_repository.patient_device_repo import PatientDeviceRepository

router = APIRouter(prefix="/patient-devices", tags=["patient-devices"])

def get_service():
    client = PgSQLClient()
    repo = PatientDeviceRepository(client)
    return PatientDeviceService(repo)

@router.post("/bind", response_model=int, status_code=status.HTTP_201_CREATED)
async def bind_device(
    pd: PatientDevice,
    service: PatientDeviceService = Depends(get_service),
):
    """
    绑定设备到患者。
    参数:
        pd (PatientDevice): 绑定关系对象，需包含 patient_id, device_id。
    返回:
        int: 新增绑定关系ID。
    异常:
        400: 参数校验失败或唯一性冲突。
        404: 患者或设备不存在。
    权限控制:
        # TODO: 如有权限需求，可在此处增加权限依赖
    """
    try:
        return await service.bind_device(pd)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="内部错误")

@router.post("/unbind/{pd_id}", response_model=bool)
async def unbind_device(
    pd_id: int,
    service: PatientDeviceService = Depends(get_service),
):
    """
    解绑患者设备关系。
    参数:
        pd_id (int): 绑定关系ID。
    返回:
        bool: 是否解绑成功（幂等）。
    异常:
        404: 绑定关系不存在。
    权限控制:
        # TODO: 如有权限需求，可在此处增加权限依赖
    """
    try:
        unbound = await service.unbind_device(pd_id)
        if not unbound:
            raise HTTPException(status_code=404, detail="Bind record not found")
        return unbound
    except Exception as e:
        raise HTTPException(status_code=500, detail="内部错误")

@router.get("/{pd_id}", response_model=PatientDevice)
async def get_patient_device(pd_id: int, service: PatientDeviceService = Depends(get_service)):
    pd = await service.get(pd_id)
    if not pd:
        raise HTTPException(status_code=404, detail="Bind record not found")
    return pd

@router.delete("/{pd_id}", response_model=bool)
async def delete_patient_device(pd_id: int, service: PatientDeviceService = Depends(get_service)):
    deleted = await service.delete(pd_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bind record not found")
    return deleted

@router.get("/", response_model=List[PatientDevice])
async def list_patient_devices(limit: int = 100, offset: int = 0, service: PatientDeviceService = Depends(get_service)):
    return await service.list(limit=limit, offset=offset)