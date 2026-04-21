from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.post import Post
from app.repositories import post_repository, company_repository
from app.schemas.posts import PostCreate, PostStatusUpdate, PostUpdate, PostFilter


def get_all(db: Session, filters: PostFilter) -> list[Post]:
    return post_repository.get_all(db, filters)


def get_by_id(db: Session, post_id: int) -> Post:
    return _get_post_or_fail(db, post_id)


def create(db: Session, data: PostCreate) -> Post:
    _check_company_exists_or_fail(db, data.company_id)
    return post_repository.create(db, data)


def update_status(db: Session, post_id: int, data:PostStatusUpdate) -> Post:
    post = _get_post_or_fail(db, post_id)
    return post_repository.update_status(db, post, data)


def update(db: Session, post_id: int, data: PostUpdate) -> Post:
    post = _get_post_or_fail(db, post_id)
    
    data_dict = data.model_dump(exclude_unset=True)
    if not data_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="fields can't be empty"
        )


    if "company_id" in data_dict:
        company_id = _get_company_id_or_fail(data_dict["company_id"])        
        if post.company_id != company_id: 
            _check_company_exists_or_fail(db, company_id)

    return post_repository.update(db, post, data)


def delete(db: Session, post_id: int) -> Post:
    post = _get_post_or_fail(db, post_id)
    return post_repository.delete(db, post)


def _get_post_or_fail(db: Session, post_id: int) -> Post:
    post = post_repository.get_by_id(db, post_id)

    if post is None:
       raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post not found"
        )
    return post


def _get_company_id_or_fail(company_id: int | None) -> int:
    if company_id is None:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="company can't be none"
            )
    return company_id

def _check_company_exists_or_fail(db: Session, company_id: int) -> None:
    company = company_repository.get_by_id(db, company_id)

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="company not found"
        )