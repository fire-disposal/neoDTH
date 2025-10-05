from app.domain.shared.base_model import DomainBaseModel
from datetime import datetime
from typing import Optional

class DeviceCreated(DomainBaseModel):
    id: int
    name: str
    type: Optional[str] = None
    serial_number: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    note: Optional[str] = None
    created_at: datetime

class DeviceUpdated(DomainBaseModel):
    id: int
    name: Optional[str] = None
    type: Optional[str] = None
    serial_number: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    note: Optional[str] = None
    updated_at: datetime

class DeviceDeleted(DomainBaseModel):
    id: int
    deleted_at: datetime