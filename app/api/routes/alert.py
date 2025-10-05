from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.adapters.pg_repository.pgsql_client import PgSQLClient
from app.adapters.pg_repository.alert_repo import HealthAlertRepository
from app.domain.alert.models import HealthAlertRecord

router = APIRouter(prefix="/alert", tags=["alert"])

def get_repo():
    client = PgSQLClient()
    return HealthAlertRepository(client)

@router.get("/", response_model=List[HealthAlertRecord])
async def list_alerts(
    patient_id: Optional[str] = Query(None, description="患者ID"),
    limit: int = Query(100, ge=1, le=200),
    offset: int = Query(0, ge=0),
    repo: HealthAlertRepository = Depends(get_repo)
):
    return await repo.list(patient_id=patient_id, limit=limit, offset=offset)

@router.get("/{alert_id}", response_model=HealthAlertRecord)
async def get_alert(
    alert_id: int,
    repo: HealthAlertRepository = Depends(get_repo)
):
    alert = await repo.get(alert_id)
    if not alert:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="告警记录不存在")
    return alert