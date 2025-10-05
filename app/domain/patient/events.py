from app.domain.shared.base_model import DomainBaseModel
from datetime import datetime
from typing import Optional

class PatientCreated(DomainBaseModel):
    id: int
    name: str
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    note: Optional[str] = None
    created_at: datetime

class PatientUpdated(DomainBaseModel):
    id: int
    name: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    note: Optional[str] = None
    updated_at: datetime

class PatientDeleted(DomainBaseModel):
    id: int
    deleted_at: datetime