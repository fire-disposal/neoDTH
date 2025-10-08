from app.domain.shared.base_model import DomainBaseModel
from datetime import datetime

class TemperatureDataReceived(DomainBaseModel):
    patient_id: str
    device_id: str
    value: float
    timestamp: datetime

class TemperatureHighAlert(DomainBaseModel):
    patient_id: str
    device_id: str
    value: float
    timestamp: datetime
    threshold: float