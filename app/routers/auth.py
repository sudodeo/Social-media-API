from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from ..alchemy_database import get_db
from .. import utils, schemas, models, oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.username == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    access_token = oauth2.create_token(data={'user_id': user.id})
    return {'token': access_token, 'token_type': 'bearer'}
