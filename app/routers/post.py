from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy import func
from typing import List
# import database
from sqlalchemy.orm import Session

from ..schemas import CreatePost, ResponsePost
from .. import oauth2, models
from ..alchemy_database import get_db


router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get('/', response_model=List[ResponsePost])
def get_posts(db: Session = Depends(get_db), limit: int = 10):
    # Using SQLAlchemy
    posts = db.query(models.Post).limit(limit).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    # Using SQL queries
    # posts = database.get_posts()
    return posts


@router.get('/{id}', response_model=ResponsePost)
def get_post(id: int, db: Session = Depends(get_db)):
    # Using SQL queries
    # post = database.get_post(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post


@router.post('/', status_code=201, response_model=ResponsePost)
def create_post(post: CreatePost, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # Using SQLAlchemy
    #  **post.dict() is unpacking the dictionary to format title=....., content=...
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # Using SQL queries
    # database.create_post(post.dict())
    return new_post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # Using SQL queries
    # return database.delete_post(id)
    # Using SQLAlchemy
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this post")
    post_query.delete()
    db.commit()
    return post


@router.put('/{id}', response_model=ResponsePost)
def update_post(id, updated_post: CreatePost, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # Using SQL queries
    # return database.update_post(id, post.dict())
    # Using SQLAlchemy
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this post")
    post_query.update(updated_post.dict())
    db.commit()
    db.refresh(post)
    return post
