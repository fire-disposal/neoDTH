from app.domain.shared.base_model import DomainBaseModel
from typing import Optional
from datetime import datetime

class SleepMeasurement(DomainBaseModel):
    patient_id: str
    device_id: str
    duration_minutes: int
    sleep_quality: Optional[str] = None
    timestamp: datetime
    note: Optional[str] = None