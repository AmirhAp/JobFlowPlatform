from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from app.core.enum import PostStatusEnum


def normalize_non_empty_title(title: str) -> str:
    title = title.strip().lower()
    if not title:
        raise ValueError("title can't be empty")
    return title


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    company_id: int = Field(..., gt=0)
    status: PostStatusEnum = Field(default=PostStatusEnum.SAVED)

    @field_validator("title")
    @classmethod
    def lower_title(cls, title: str) -> str:
        return normalize_non_empty_title(title)


class PostRead(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=0, max_length=200)
    company_id: Optional[int] = Field(default=None, gt=0)

    @field_validator("title")
    @classmethod
    def normalize_title(cls, title):
        if title is None:
            return None
        return normalize_non_empty_title(title)

class PostStatusUpdate(BaseModel):
    status: PostStatusEnum


class PostFilter(BaseModel):
    status: Optional[PostStatusEnum] = None
    company_id: Optional[int] = Field(default=None, gt=0)
    skip: Optional[int] = Field(default=0, ge=0)
    limit: Optional[int] = Field(default=100, gt=0, le=100)