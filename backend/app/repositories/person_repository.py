from sqlalchemy.orm import Session

from app.models.person import Person
from app.schemas.persons import PersonCreate, PersonInfoUpdate, PersonStatusUpdate


def get_by_id(db: Session, person_id: int) -> Person | None:
    return db.query(Person).filter(Person.id == person_id).first()


def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Person]:
    return db.query(Person).offset(skip).limit(limit).all()


def create(db: Session, data: PersonCreate) -> Person:
    person = Person(**data.model_dump())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


def update(db: Session, person: Person, data: PersonInfoUpdate) -> Person:
    data_dict = data.model_dump(exclude_unset=True)

    if not data_dict:
        return person

    for field, value in data_dict.items():
        setattr(person, field, value)

    db.commit()
    db.refresh(person)
    return person


def update_status(db: Session, person: Person, data: PersonStatusUpdate) -> Person:
    person.status = data.status
    db.commit()
    db.refresh(person)
    return person


def delete(db: Session, person: Person) -> Person:
    db.delete(person)
    db.commit()
    return person
