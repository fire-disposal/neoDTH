from app.domain.shared.base_model import DomainBaseModel
from typing import Optional

class Device(DomainBaseModel):
    """
    设备领域模型。
    字段:
        id: 设备ID
        name: 设备名称（必填）
        type: 设备类型
        serial_number: 序列号（必填，唯一）
        manufacturer: 厂商
        model: 型号
        note: 备注
    权限控制预留: 可在此模型扩展 owner_id/tenant_id 字段用于多租户/权限控制。
    """
    id: Optional[int] = None
    name: str
    type: Optional[str] = None
    serial_number: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    note: Optional[str] = None