from app.domain.shared.repository import IRepository
from .models import PatientDevice

class IPatientDeviceRepository(IRepository[PatientDevice]):
    pass