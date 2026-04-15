from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CompanyBase(BaseModel):
    name: str


class CompanyCreate(CompanyBase):
    pass 


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CompanyUpdate(BaseModel):
    name: Optional[str] = None



