from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, ForeignKey, Enum
from datetime import datetime
from app.db.session import Base
from app.core.enum import PostStatusEnum


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
       primary_key=True, 
       index=True
    )

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"), 
        nullable=False,
        index=True
    )
    
    status: Mapped[PostStatusEnum] = mapped_column(
        Enum(PostStatusEnum), 
        nullable=False, 
        default=PostStatusEnum.SAVED,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False
    )