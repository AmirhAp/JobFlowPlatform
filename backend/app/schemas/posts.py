from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from app.core.enum import PostStatusEnum


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    company_id: int
    status: PostStatusEnum

    @field_validator("title")
    def lower_title(cls, title):
        return title.strip().lower()


class PostRead(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    company_id: Optional[int] = None
    status: Optional[PostStatusEnum] = None

    @field_validator("title")
    def normalize_title(cls, title):
        if title is not None:
            return title.stip().lower()
        return title


class PostStatusUpdate(BaseModel):
    status: PostStatusEnum


    
