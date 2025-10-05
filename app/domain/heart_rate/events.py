from app.domain.shared.base_model import DomainBaseModel
from datetime import datetime

class HeartRateDataReceived(DomainBaseModel):
    patient_id: str
    device_id: str
    value: int
    timestamp: datetime

class HeartRateHighAlert(DomainBaseModel):
    patient_id: str
    device_id: str
    value: int
    timestamp: datetime
    threshold: int