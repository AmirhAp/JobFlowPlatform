from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.session import Base


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, default="applied")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)