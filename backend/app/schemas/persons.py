from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.core.enum import PersonStatus
from datetime import datetime

class PersonBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    company_id: int
    status: PersonStatus

    @field_validator("name")
    def normalize_name(cls, name):
        return name.strip().lower()


class PersonRead(PersonBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
    

class PersonCreate(PersonBase):
    pass 


class PersonStatusUpdate(BaseModel):
    status: PersonStatus


class PersonInfoUpdate(BaseModel):
    name: Optional[str] = None
    company_id: Optional[int] = None

    @field_validator("name")
    def normalize_name(cls, name):
        if name is not None:
            return name.strip().lower()
        return name
