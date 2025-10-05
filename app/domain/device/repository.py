from app.domain.shared.repository import IRepository
from .models import Device

class IDeviceRepository(IRepository[Device]):
    pass