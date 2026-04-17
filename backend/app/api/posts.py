from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from app.core.enum import PostStatus

from app.schemas.posts import PostRead, PostCreate, PostUpdate, PostStatusUpdate


router = APIRouter(prefix="/posts", tags=["posts"])


db = []
current_id = 1

def find_post(post_id: int) -> dict | None:
    for post in db: 
        if post["id"] == post_id:
            return post
    return None


@router.get("/", response_model=List[PostRead])
def get_all_posts(status: Optional[PostStatus] = Query(default=None),
                  company_id: Optional[int] = Query(default=None)):
    posts = list(db)

    if status is not None: 
        posts = [post for post in posts if post["status"] == status]

    if company_id is not None: 
        posts = [post for post in posts if post["company_id"] == company_id]

    return posts


@router.get("/{post_id}", response_model=PostRead)
def get_post_by_id(post_id: int):
    post = find_post(post_id)

    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    
    return post


@router.post("/", response_model=PostRead)
def create_post(post: PostCreate):
    global current_id
    now = datetime.utcnow()

    new_post = {
        "id": current_id,
        "title": post.title,
        "company_id": post.company_id,
        "status": post.status,
        "created_at": now,
        "updated_at": now
    }
    current_id += 1
    db.append(new_post)

    return new_post


@router.patch("/{post_id}/status", response_model=PostRead)
def update_post_status(post_id: int, updated_status_post: PostStatusUpdate):
    post = find_post(post_id)

    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    
    post["status"] = updated_status_post.status
    post["updated_at"] = datetime.utcnow()
    
    return post


@router.put("/{post_id}", response_model=PostRead)
def update_post_info(post_id: int, updated_post: PostUpdate):
    post = find_post(post_id)
    
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    
    if updated_post.title is not None:
        post["title"] = updated_post.title
    
    if updated_post.company_id is not None:
        post["company_id"] = updated_post.company_id

    if updated_post.status is not None:
        post["status"] = updated_post.status
    
    post["updated_at"] = datetime.utcnow()
    
    return post


@router.delete("/{post_id}", response_model=PostRead)
def remove_post(post_id: int):
    post = find_post(post_id)

    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    
    db.remove(post)

    return post