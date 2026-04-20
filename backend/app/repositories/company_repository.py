from sqlalchemy.orm import Session

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Company]:
    return db.query(Company).offset(skip).limit(limit).all()


def get_by_name(db: Session, name: str) -> Company | None:
    return db.query(Company).filter(Company.name == name).first()


def get_by_id(db: Session, company_id: int) -> Company | None:
    return db.query(Company).filter(Company.id == company_id).first()


def create(db: Session, data: CompanyCreate) -> Company:
    new_company = Company(**data.model_dump())
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


def update(db: Session, company: Company, data: CompanyUpdate) -> Company:
    data_dict = data.model_dump(exclude_unset=True)

    if not data_dict:
        return company

    for field, value in data_dict.items():
        setattr(company, field, value)

    db.commit()
    db.refresh(company)
    return company


def delete(db: Session, company: Company) -> Company:
    db.delete(company)
    db.commit()
    return company