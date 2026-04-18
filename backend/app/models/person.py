from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, ForeignKey, Enum
from datetime import datetime
from app.db.session import Base
from app.core.enum import PersonStatus


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    status: Mapped[PersonStatus] = mapped_column(
        Enum(PersonStatus), 
        nullable=False, 
        default=PersonStatus.SAVED
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)