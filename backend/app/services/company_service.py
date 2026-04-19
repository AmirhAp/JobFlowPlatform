from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.schemas.company import CompanyCreate, CompanyUpdate
from app.models.company import Company
from backend.app.repositories import company_repository


def check_for_id(db: Session, id: int) -> None:
    company = company_repository.get_by_id(db, id)
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="company not found"
        )


def check_for_name(db: Session, name: str) -> None:
    company = company_repository.get_by_name(db, name)
    if company is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="company already exists"
        )


def get_all(db: Session) -> List[Company]:
    return company_repository.get_all(db)


def create(db: Session, data: CompanyCreate) -> Company:
    check_for_name(db, data.name)
    
    try: 
        company = company_repository.create(db, data)
        return company
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="company already exists"
        )


def edit(db: Session, id: int, updated_company: CompanyUpdate) -> Company:
    check_for_id(db, id)

    if updated_company.name:
        check_for_name(db, updated_company.name)
    
    try: 
        updated_company = company_repository.edit(db, id, updated_company)
        return updated_company
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="company name already exists"
        )
    

def delete(db: Session, id: int) -> Company:
    check_for_id(db, id)

    try: 
        deleted_company = company_repository.delete(db, id)
        return deleted_company
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="company not found"
        )