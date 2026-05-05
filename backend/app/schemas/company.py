from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from typing import Optional


class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=32)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, name: str) -> str:
        name = name.strip().lower()
        
        if not name:
            raise ValueError("company name can not be empty")
        return name


class CompanyCreate(CompanyBase):
    pass 


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=32)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, name: str | None) -> str | None:
        if name is None:
            return None
        
        name = name.strip().lower()

        if not name:
            raise ValueError("company name can not be empty")
        
        return name


