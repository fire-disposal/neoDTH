from app.domain.shared.base_model import DomainBaseModel
from typing import Optional

class PatientDevice(DomainBaseModel):
    """
    患者设备绑定关系模型。
    属性:
        id (Optional[int]): 绑定关系ID
        patient_id (int): 患者ID
        device_id (int): 设备ID
        bind_time (Optional[str]): 绑定时间（ISO格式字符串）
        unbind_time (Optional[str]): 解绑时间（ISO格式字符串）
        note (Optional[str]): 备注
    """
    id: Optional[int] = None
    patient_id: int
    device_id: int
    bind_time: Optional[str] = None
    unbind_time: Optional[str] = None
    note: Optional[str] = None