from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.hash import Hash
from schemas import UserBase, UserDisplay, UserLogin
from db.database import get_db
from db import db_user

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/register', response_model=UserDisplay)
def register_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


@router.post('/login', response_model=UserDisplay)
def login(request: UserLogin, db: Session = Depends(get_db)):
    user = db_user.get_user_by_email(db, request.email)
    if not user or not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user


@router.get('/{id}', response_model=UserDisplay)
def read_user(id: int, db: Session = Depends(get_db)):
    user = db_user.get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put('/{id}', response_model=UserDisplay)
def update_user(id: int, request: UserBase, db: Session = Depends(get_db)):
    user = db_user.update_user_in_db(db, id, request)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete('/{id}', response_model=dict)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db_user.delete_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
