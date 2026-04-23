from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.persons import PersonRead, PersonCreate, PersonInfoUpdate, PersonStatusUpdate, PersonFilters
from app.services import person_service
from app.db.dependencies import get_db


router = APIRouter(prefix="/persons", tags=["persons"])


@router.get("/", response_model=List[PersonRead])
def get_all_persons(filters: PersonFilters = Depends(), db: Session = Depends(get_db)):
    return person_service.get_all(db, filters)


@router.get("/{person_id}", response_model=PersonRead)
def get_person_by_id(person_id: int, db: Session = Depends(get_db)):
    return person_service.get_by_id(db, person_id)


@router.post("/", response_model=PersonRead)
def create_person(person: PersonCreate, db: Session=Depends(get_db)):
    return person_service.create(db, person)


@router.put("/{person_id}", response_model=PersonRead)
def update_person_info(person_id: int, data: PersonInfoUpdate, db: Session=Depends(get_db)):
    return person_service.update(db, person_id, data)


@router.patch("/{person_id}/status", response_model=PersonRead)
def update_person_status(person_id: int, data: PersonStatusUpdate, db: Session=Depends(get_db)):
    return person_service.update_status(db, person_id, data)


@router.delete("/{person_id}", response_model=PersonRead)
def remove_person(person_id: int, db: Session=Depends(get_db)):
    return person_service.delete(db, person_id)