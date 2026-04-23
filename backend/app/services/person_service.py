from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from app.repositories import person_repository, company_repository
from app.models.person import Person
from app.schemas.persons import PersonFilters, PersonCreate, PersonInfoUpdate, PersonStatusUpdate


def get_all(db: Session, filters: PersonFilters) -> list[Person]:
    return person_repository.get_all(db, filters) 


def get_by_id(db: Session, person_id: int) -> Person:
    return _get_person_or_fail(db, person_id)


def create(db: Session, data: PersonCreate) -> Person:
    _check_company_exists_or_fail(db, data.company_id)
    return person_repository.create(db, data)
    

def update(db: Session, person_id: int, data: PersonInfoUpdate) -> Person:
    person = _get_person_or_fail(db, person_id)

    data_dict = data.model_dump(exclude_unset=True)
    if not data_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no field to update"
        )

    if "company_id" in data_dict:
        company_id = data_dict["company_id"]
        _check_company_id_not_none_or_fail(company_id)
        
        if person.company_id != company_id:
            _check_company_exists_or_fail(db, company_id)

    person.updated_at = datetime.utcnow()
    return person_repository.update(db, person, data) 


def update_status(db: Session, person_id: int, data: PersonStatusUpdate) -> Person:
    person = _get_person_or_fail(db, person_id)
    person.updated_at = datetime.utcnow() 
    return person_repository.update_status(db, person, data)


def delete(db: Session, person_id: int) -> Person:
    person = _get_person_or_fail(db, person_id)
    return person_repository.delete(db, person)
    

def _get_person_or_fail(db: Session, person_id: int) -> Person:
    person = person_repository.get_by_id(db, person_id)

    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="person not found"
        )
    return person


def _check_company_id_not_none_or_fail(company_id: int | None) -> None:
    if company_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="company can't be none"
        )


def _check_company_exists_or_fail(db: Session, company_id: int) -> None:
    company = company_repository.get_by_id(db, company_id)
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="company not found"
        )
