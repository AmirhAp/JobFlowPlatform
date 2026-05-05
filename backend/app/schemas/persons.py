from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.core.enum import PersonStatusEnum
from datetime import datetime


def normalize_none_empty_name(name: str) -> str:
    name = name.strip().lower()
    if not name: 
        raise ValueError("name can't be empty")
    return name


class PersonBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    company_id: int = Field(..., gt=0)
    status: PersonStatusEnum = Field(default=PersonStatusEnum.SAVED)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, name: str) -> str:
        return normalize_none_empty_name(name)


class PersonRead(PersonBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
    

class PersonCreate(PersonBase):
    pass 


class PersonStatusUpdate(BaseModel):
    status: PersonStatusEnum


class PersonInfoUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    company_id: Optional[int] = Field(default=None, gt=0)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, name: str | None) -> str | None:
        if name is None:
           return None
        return normalize_none_empty_name(name) 


class PersonFilters(BaseModel):
    status: Optional[PersonStatusEnum] = None
    company_id: Optional[int] = Field(default=None, gt=0)
    skip: Optional[int] = Field(default=0, ge=0)
    limit: Optional[int] = Field(default=100, gt=0, le=100)
    