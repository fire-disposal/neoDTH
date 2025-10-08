from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

def utcnow_factory() -> datetime:
    # 统一使用带时区的 UTC 时间
    return datetime.now(timezone.utc)

class InfluxDataBaseModel(BaseModel):
    # 🌟 必需的 Tag 字段，用于高效查询和索引
    patient_id: str = Field(..., description="患者ID (InfluxDB Tag)")
    device_id: str = Field(..., description="设备ID (InfluxDB Tag)")
    
    # 核心时间戳：事件发生的时间
    # ⚠️ 必须是非可选的 (datetime)，并带 default_factory
    measured_at: datetime = Field(
        default_factory=utcnow_factory, 
        description="测量/事件发生时间 (InfluxDB Timestamp)"
    )
    
    # 可选审计字段：记录进入系统的时间 (InfluxDB Field)
    created_at: datetime = Field(
        default_factory=utcnow_factory, 
        description="数据点创建时间 (InfluxDB Field)"
    )

    class Config:
        from_attributes = True
        validate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}



