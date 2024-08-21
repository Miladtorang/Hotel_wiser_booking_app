from fastapi import APIRouter, HTTPException, status
from db.hash import Hash
from schemas import TokenBase
from db.database import get_db
from db import db_user
from db.models import DbUser
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from auth import oauth2

router = APIRouter(
    prefix='/tokens',
    tags=['authentication']
)


@router.post('/')
def get_token(request: OAuth2PasswordBearer = Depends(), db: Session = Depends(get_db)):
    user = db_user.get_user_by_username(db, request.username)
    # user = db.query(models.DbUser).filter(DbUser.user_name == request.username).first()
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
