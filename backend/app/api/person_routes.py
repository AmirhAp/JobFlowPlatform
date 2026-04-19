from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from app.schemas.persons import PersonRead, PersonCreate, PersonInfoUpdate, PersonStatusUpdate
from app.core.enum import PersonStatusEnum
from datetime import datetime

router = APIRouter(prefix="/persons", tags=["persons"])


db = []
current_index = 1

def find_person(person_id: int) -> dict | None:
    for person in db:
        if person["id"] == person_id:
            return person
    return None


@router.get("/", response_model=List[PersonRead])
def get_all_persons(status: Optional[PersonStatusEnum] = Query(default=None)):
    persons = list(db)

    if status is not None:
        persons = [person for person in persons if person["status"] == status]

    return persons


@router.get("/{person_id}", response_model=PersonRead)
def get_person_by_id(person_id: int):
    person = find_person(person_id)

    if person is None:
        raise HTTPException(status_code=404, detail="person not found")

    return person


@router.post("/", response_model=PersonRead)
def create_person(person: PersonCreate):
    global current_index
    now = datetime.utcnow()


    new_person = {
        "id": current_index,
        "name": person.name,
        "company_id": person.company_id,
        "status": person.status,
        "created_at": now, 
        "updated_at": now
    }
    db.append(new_person)
    current_index += 1

    return new_person


@router.put("/{person_id}", response_model=PersonRead)
def update_person_info(person_id: int, updated_person: PersonInfoUpdate):
    person = find_person(person_id)

    if person is None:
        raise HTTPException(status_code=404, detail="person not found")
    
    if updated_person.name is not None:
        person["name"] = updated_person.name
    
    if updated_person.company_id is not None:
        person["company_id"] = updated_person.company_id

    person["updated_at"] = datetime.utcnow()

    return person


@router.patch("/{person_id}/status", response_model=PersonRead)
def update_person_status(person_id: int, updated_person_status: PersonStatusUpdate):
    person = find_person(person_id)

    if person is None:
        raise HTTPException(status_code=404, detail="person not found")

    person["status"] = updated_person_status.status
    person["updated_at"] = datetime.utcnow()

    return person


@router.delete("/{person_id}", response_model=PersonRead)
def remove_person(person_id: int):
    person = find_person(person_id)

    if person is None:
        raise HTTPException(status_code=404, detail="person not found")

    db.remove(person)
    return person