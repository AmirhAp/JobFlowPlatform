from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, ForeignKey, Enum
from datetime import datetime
from app.db.session import Base
from app.core.enum import PersonStatusEnum


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"), 
        nullable=False,
        index=True
    )

    status: Mapped[PersonStatusEnum] = mapped_column(
        Enum(PersonStatusEnum), 
        nullable=False, 
        default=PersonStatusEnum.SAVED,
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
        nullable=False,
        onupdate=datetime.utcnow
    )