from sqlalchemy.orm import Session
from db.models import DbUser
from schemas import UserBase
from db.hash import Hash
from fastapi import HTTPException, status


def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        user_name=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session):
    return db.query(DbUser).all()


def get_user(db: Session, username: int):
    return db.query(DbUser).filter(DbUser.id == id).first()


def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.user_name == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with username{username} not found')
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(DbUser).filter(DbUser.email == email).first()


def update_user_in_db(db: Session, id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if user:
        user.user_name = request.username
        user.email = request.email
        user.password = Hash.bcrypt(request.password)
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
