from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DomainBaseModel(BaseModel):
    id: Optional[str] = Field(None, description="唯一标识")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="更新时间")

    class Config:
        from_attributes = True
        validate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}