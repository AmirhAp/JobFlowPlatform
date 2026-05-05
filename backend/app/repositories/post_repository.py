from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.posts import PostCreate, PostUpdate, PostStatusUpdate, PostFilter


def get_by_id(db: Session, post_id: int) -> Post | None:
    return db.query(Post).filter(Post.id == post_id).first()


def get_all(db: Session, filters: PostFilter) -> list[Post]:
    query = db.query(Post)

    if filters.company_id is not None:
        query = query.filter(Post.company_id == filters.company_id)
    
    if filters.status is not None:
        query = query.filter(Post.status == filters.status)
    
    return query.offset(filters.skip).limit(filters.limit).all()


def create(db: Session, data: PostCreate) -> Post:
    post = Post(**data.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def update_status(db: Session, post: Post, data: PostStatusUpdate) -> Post:
    post.status = data.status
    db.commit()
    db.refresh(post)
    return post


def update(db: Session, post: Post, data: PostUpdate) -> Post:
    data_dict = data.model_dump(exclude_unset=True)

    for field, value in data_dict.items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)
    return post


def delete(db: Session, post: Post) -> Post:
    db.delete(post)
    db.commit()
    return post