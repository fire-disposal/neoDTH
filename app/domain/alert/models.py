from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field
from app.domain.shared.base_model import utcnow_factory

from app.domain.shared.base_model import DomainBaseModel

class HealthAlertRecord(DomainBaseModel):
    patient_id: str
    device_id: Optional[str] = None
    alert_type: str
    alert_level: str
    message: str
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    extra: Optional[dict] = None