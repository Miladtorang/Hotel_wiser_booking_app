from fastapi import APIRouter, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import models
from db.hash import Hash
from auth import oauth2

router = APIRouter(
    tags=['authentication']
)


# token
@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.DbUser).filter(models.DbUser.user_name == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid credentials')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='incorrect password')

    access_token = oauth2.create_access_token(data={'sub': user.user_name})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'user_name': user.user_name
    }
