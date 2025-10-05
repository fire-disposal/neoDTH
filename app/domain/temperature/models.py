from app.domain.shared.base_model import DomainBaseModel
from typing import Optional
from datetime import datetime

class TemperatureMeasurement(DomainBaseModel):
    patient_id: str
    device_id: str
    value: float
    timestamp: datetime
    note: Optional[str] = None