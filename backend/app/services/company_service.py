from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.schemas.company import CompanyCreate, CompanyUpdate
from app.models.company import Company
from app.repositories import company_repository


NOT_FOUND_404 = "company not found"
ALREAT_EXISTS_400 = "company already exitst"


def get_all(db: Session) -> List[Company]:
    return company_repository.get_all(db)


def create(db: Session, data: CompanyCreate) -> Company:
    _ensure_name_is_available (db, data.name)
    
    try: 
        return company_repository.create(db, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = ALREAT_EXISTS_400
        )
    

def update(db: Session, company_id: int, updated_company: CompanyUpdate) -> Company:
    company = _get_company_or_404(db, company_id)

    if updated_company.name is not None:
        _ensure_name_is_available(db, updated_company.name, company.id)

    try: 
        return company_repository.update(db, company, updated_company)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ALREAT_EXISTS_400
        )
    

def delete(db: Session, company_id: int) -> Company:
    company = _get_company_or_404(db, company_id)
    return company_repository.delete(db, company)

    

def _get_company_or_404 (db: Session, company_id: int) -> Company:
    company = company_repository.get_by_id(db, company_id)
    if company is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = NOT_FOUND_404
        )
    return company


def _ensure_name_is_available (db: Session, name: str, exlude_company_id: int | None = None) -> None:
    existing_company = company_repository.get_by_name(db, name)
    
    if existing_company is None:
        return 
    
    if existing_company is not None and existing_company.id == exlude_company_id:
        return 
    
    raise HTTPException(
        status_code = status.HTTP_400_BAD_REQUEST, 
        detail = ALREAT_EXISTS_400
    )
