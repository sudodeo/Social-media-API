from fastapi import HTTPException, status, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
import sqlalchemy.exc

from ..schemas import CreateUser, ResponseUser
from ..alchemy_database import get_db
from .. import oauth2, models, utils


router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ResponseUser)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Email/ username has been used')

    return new_user


@router.get('/', response_model=List[ResponseUser])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/{id}', response_model=ResponseUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id {id} does not exist')

    return user


@router.put('/{id}', response_model=ResponseUser)
def update_user(id: int, updated_user: CreateUser, user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id {id} does not exist')
    user_query.update(updated_user.dict())
    db.commit()
    db.refresh(user)
    return user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} does not exist')

    user_query.delete()
    db.commit()
    return user
