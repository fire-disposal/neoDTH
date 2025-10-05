from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class HealthAlertRecord(BaseModel):
    id: Optional[int] = None
    patient_id: str
    device_id: Optional[str] = None
    alert_type: str
    alert_level: str
    message: str
    created_at: datetime = datetime.utcnow()
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    extra: Optional[dict] = None

    class Config:
        from_attributes = True