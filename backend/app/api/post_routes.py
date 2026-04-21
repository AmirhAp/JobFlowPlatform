from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.posts import PostRead, PostCreate, PostUpdate, PostStatusUpdate, PostFilter
from app.db.dependencies import get_db
from app.services import post_service

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[PostRead])
def get_all_posts(filter: PostFilter = Depends(),db: Session = Depends(get_db)):
    return post_service.get_all(db, filter)


@router.get("/{post_id}", response_model=PostRead)
def get_post_by_id(post_id: int, db: Session=Depends(get_db)):
    return post_service.get_by_id(db, post_id)


@router.post("/", response_model=PostRead)
def create_post(post: PostCreate, db: Session=Depends(get_db)):
    return post_service.create(db, post)


@router.patch("/{post_id}/status", response_model=PostRead)
def update_post_status(post_id: int, data: PostStatusUpdate, db: Session=Depends(get_db)):
    return post_service.update_status(db, post_id, data)    


@router.put("/{post_id}", response_model=PostRead)
def update_post_info(post_id: int, data: PostUpdate, db: Session=Depends(get_db)):
    return post_service.update(db, post_id, data)


@router.delete("/{post_id}", response_model=PostRead)
def remove_post(post_id: int, db: Session=Depends(get_db)):
    return post_service.delete(db, post_id)
   