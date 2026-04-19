from sqlalchemy.orm import Session
from typing import List
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


def get_all(db: Session, skip: int = 0, limit: int = 0) -> List[Company]:
    return db.query(Company).offset(skip).limit(limit).all()


def get_by_name(db: Session, name: str) -> Company | None:
    return db.query(Company).filter(Company.name == name).first()


def get_by_id(db: Session, id: int) -> Company | None:
    return db.query(Company).filter(Company.id == id).first()


def create(db: Session, data: CompanyCreate) -> Company:
    new_company = Company(**data.model_dump())

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company


def edit(db: Session, id: int, data: CompanyUpdate) -> Company:
    pass


def delete(db: Session, id: int) -> Company:
    pass