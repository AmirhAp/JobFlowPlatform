from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.core.enum import PostStatus


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    company_id: int
    status: PostStatus


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
    status: Optional[PostStatus] = None


class PostStatusUpdate(BaseModel):
    status: PostStatus


    
