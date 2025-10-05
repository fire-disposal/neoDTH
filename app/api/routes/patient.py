from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.domain.patient.models import Patient
from app.services.patient_service import PatientService
from app.adapters.pg_repository.pgsql_client import PgSQLClient
from app.adapters.pg_repository.patient_repo import PatientRepository
from app.core.logger import get_logger

logger = get_logger("patient_api")

router = APIRouter(prefix="/patients", tags=["patients"])

def get_service():
    client = PgSQLClient()
    repo = PatientRepository(client)
    return PatientService(repo)

@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient: Patient,
    service: PatientService = Depends(get_service),
):
    """
    创建患者。
    Args:
        patient (Patient): 患者对象，需校验姓名、手机号等字段
    Returns:
        int: 新增患者ID
    """
    try:
        # 权限控制预留：如需权限校验，可在此处添加依赖
        return await service.create_patient(patient)
    except ValueError as ve:
        logger.warning(f"参数校验失败: {ve}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"创建患者异常: {e}")
        raise HTTPException(status_code=500, detail="创建患者失败")

@router.get("/{patient_id}", response_model=Patient)
async def get_patient(
    patient_id: int,
    service: PatientService = Depends(get_service),
):
    """
    获取患者信息。
    Args:
        patient_id (int): 患者ID
    Returns:
        Patient: 患者对象
    """
    try:
        patient = await service.get_patient(patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取患者异常: {e}")
        raise HTTPException(status_code=500, detail="获取患者失败")

@router.put("/{patient_id}", response_model=bool)
async def update_patient(
    patient_id: int,
    patient: Patient,
    service: PatientService = Depends(get_service),
):
    """
    更新患者信息。
    Args:
        patient_id (int): 患者ID
        patient (Patient): 新患者数据
    Returns:
        bool: 是否更新成功
    """
    try:
        updated = await service.update_patient(patient_id, patient)
        if not updated:
            raise HTTPException(status_code=404, detail="Patient not found")
        return updated
    except ValueError as ve:
        logger.warning(f"参数校验失败: {ve}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"更新患者异常: {e}")
        raise HTTPException(status_code=500, detail="更新患者失败")

@router.delete("/{patient_id}", response_model=bool)
async def delete_patient(
    patient_id: int,
    service: PatientService = Depends(get_service),
):
    """
    删除患者信息。
    Args:
        patient_id (int): 患者ID
    Returns:
        bool: 是否删除成功
    """
    try:
        deleted = await service.delete_patient(patient_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Patient not found")
        return deleted
    except Exception as e:
        logger.error(f"删除患者异常: {e}")
        raise HTTPException(status_code=500, detail="删除患者失败")

@router.get("/", response_model=List[Patient])
async def list_patients(
    limit: int = 100,
    offset: int = 0,
    service: PatientService = Depends(get_service),
):
    """
    分页获取患者列表。
    Args:
        limit (int): 每页数量
        offset (int): 偏移量
    Returns:
        List[Patient]: 患者列表
    """
    try:
        return await service.list_patients(limit=limit, offset=offset)
    except Exception as e:
        logger.error(f"获取患者列表异常: {e}")
        raise HTTPException(status_code=500, detail="获取患者列表失败")

# 权限控制说明：如需对接口增加权限控制，可在依赖项中添加权限依赖，如 Depends(get_current_user)