from app.domain.shared.base_model import DomainBaseModel
from datetime import datetime
from typing import Optional

class SleepDataReceived(DomainBaseModel):
    patient_id: str
    device_id: str
    duration_minutes: int
    sleep_quality: Optional[str] = None
    timestamp: datetime

class SleepQualityAlert(DomainBaseModel):
    patient_id: str
    device_id: str
    duration_minutes: int
    sleep_quality: Optional[str] = None
    timestamp: datetime
    threshold: Optional[str] = None