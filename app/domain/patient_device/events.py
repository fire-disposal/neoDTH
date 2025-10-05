from app.domain.shared.base_model import DomainBaseModel
from datetime import datetime
from typing import Optional

class PatientDeviceBound(DomainBaseModel):
    id: int
    patient_id: int
    device_id: int
    bind_time: datetime

class PatientDeviceUnbound(DomainBaseModel):
    id: int
    patient_id: int
    device_id: int
    unbind_time: datetime