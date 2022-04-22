from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
import schemas
from typing import List
import models
import database
from sqlalchemy.orm import Session
import oauth2
from alchemy_database import get_db


router = APIRouter(prefix='/votes', tags=['Votes'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(user_vote: schemas.Vote, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == user_vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if user_vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already voted on post"
                                )
        new_vote = models.Vote(post_id=user_vote.post_id,
                               user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote to post"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete()
        db.commit()

        return {"message": "Successfully deleted vote"}
