from app.domain.shared.base_model import DomainBaseModel
from typing import Optional
from datetime import datetime

class HeartRateMeasurement(DomainBaseModel):
    patient_id: str
    device_id: str
    value: int
    timestamp: datetime
    note: Optional[str] = None