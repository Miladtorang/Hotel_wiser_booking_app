from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.hash import Hash
from schemas import UserBase, UserDisplay
from db.database import get_db
from db import db_user
from auth.oauth2 import get_current_user
from db.models import DbUser

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('', response_model=UserDisplay, status_code=201)
def register_user(request: UserBase, db: Session = Depends(get_db)):
    user = request.username
    existing_user = None
    
    try:
        existing_user = db_user.get_user_by_username(db, user)
    except:
        pass

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

        
    return db_user.create_user(db, request)



@router.get('/{id}', response_model=UserDisplay, status_code=200)
def read_user(id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    user = db_user.get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized")
    return user


@router.put('/{id}', response_model=UserDisplay, status_code=200)
def update_user(
        id: int,
        request: UserBase,
        db: Session = Depends(get_db),
        current_user: DbUser = Depends(get_current_user)
):
    user = db_user.get_user(db, id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized")

    user = db_user.update_user_in_db(db, id, request)

    return user


@router.delete('/{id}', status_code=204)
def delete_user(id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    user = db_user.get_user(db, id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized")
    db_user.delete_user(db, id)
    return
