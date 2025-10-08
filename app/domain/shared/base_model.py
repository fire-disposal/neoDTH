from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

def utcnow_factory() -> datetime:
    return datetime.now(timezone.utc)

class DomainBaseModel(BaseModel):
    id: Optional[str] = Field(default=None, description="唯一标识")
    created_at: Optional[datetime] = Field(
        default_factory=utcnow_factory,
        description="创建时间 (UTC)"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=utcnow_factory,
        description="更新时间 (UTC)"
    )

    class Config:
        from_attributes = True
        validate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}