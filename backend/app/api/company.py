from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate


router = APIRouter(prefix="/companies", tags=["companies"])

#for testing
db = []
current_id = 1


def find_company(company_id: int) -> dict | None:
    for company in db: 
        if company["id"] == company_id:
            return company
    return None


@router.get("/", response_model=List[CompanyRead])
def all_companies():
    return db


@router.post("/", response_model=CompanyRead)
def create_company(new_company: CompanyCreate):
    global current_id

    company = {
        "id" : current_id,
        "name": new_company.name,
        "created_at" : datetime.utcnow()
    }
    db.append(company)
    current_id += 1

    return company


@router.put("/{company_id}", response_model=CompanyRead)
def update_compnay(company_id: int, updated_company: CompanyUpdate):
    company = find_company(company_id)

    if company is None:
        raise HTTPException(status_code=404, detail="company doesn't exist")
    
    if updated_company.name is not None:
        company["name"] = updated_company.name

    return company


@router.delete("/{company_id}", response_model=CompanyRead)
def remove_company(company_id: int):
    company = find_company(company_id)

    if company is None: 
        raise HTTPException(status_code=404, detail="company doesn't exist")
    
    db.remove(company)

    return company

