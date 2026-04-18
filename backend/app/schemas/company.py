from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class CompanyBase(BaseModel):
    name: str

    @field_validator("name")
    def normalize_name(cls, name):
        return name.strip().lower()


class CompanyCreate(CompanyBase):
    pass 


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CompanyUpdate(BaseModel):
    name: Optional[str] = None

    @field_validator("name")
    def normalize_name(cls, name):
        if name is not None:
            return name.strip().lower()
        return name


