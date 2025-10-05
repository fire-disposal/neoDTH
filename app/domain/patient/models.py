from app.domain.shared.base_model import DomainBaseModel
from typing import Optional
from datetime import date
from pydantic import Field, validator
import re

class Patient(DomainBaseModel):
    """
    患者领域模型。
    Attributes:
        id: 患者ID，数据库自增主键
        name: 姓名，必填
        gender: 性别，可选
        birth_date: 出生日期，可选
        phone: 手机号，可选，格式校验
        address: 地址，可选
        note: 备注，可选
    """
    id: Optional[int] = Field(default=None, description="患者ID")
    name: str = Field(..., description="姓名", min_length=1)
    gender: Optional[str] = Field(default=None, description="性别")
    birth_date: Optional[date] = Field(default=None, description="出生日期")
    phone: Optional[str] = Field(default=None, description="手机号")
    address: Optional[str] = Field(default=None, description="地址")
    note: Optional[str] = Field(default=None, description="备注")

    @validator("name")
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("姓名不能为空")
        return v

    @validator("phone")
    def phone_format_check(cls, v):
        if v is None or v == "":
            return v
        # 简单手机号格式校验（中国大陆）
        if not re.match(r"^1[3-9]\d{9}$", v):
            raise ValueError("手机号格式不正确")
        return v