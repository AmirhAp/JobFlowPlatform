from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate
from app.db.dependencies import get_db
from app.services import company_service


router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/", response_model=List[CompanyRead])
def all_companies(db: Session = Depends(get_db)):
    return company_service.get_all(db)


@router.post("/", response_model=CompanyRead)
def create_company(new_company: CompanyCreate, db: Session = Depends(get_db)):
    return company_service.create(db, new_company)


@router.put("/{company_id}", response_model=CompanyRead)
def update_compnay(company_id: int, updated_company: CompanyUpdate, db: Session = Depends(get_db)):
    return company_service.update(db, company_id, updated_company)


@router.delete("/{company_id}", response_model=CompanyRead)
def remove_company(company_id: int, db: Session = Depends(get_db)):
    return company_service.delete(db, company_id)

