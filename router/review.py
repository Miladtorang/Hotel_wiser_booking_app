from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ReviewBase, ReviewDisplay, UserDisplay
from db.database import get_db
from db import db_review
from auth.oauth2 import get_current_user
from db.models import DbUser, DbReview

router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)


@router.post('/', response_model=ReviewDisplay)
def create_review_endpoint(request: ReviewBase, db: Session = Depends(get_db),
                           current_user: DbUser = Depends(get_current_user)):
    user_id = current_user.id
    return db_review.create_review(db, request, user_id)


@router.get('/', response_model=List[ReviewDisplay])
def list_reviews(db: Session = Depends(get_db)):
    return db_review.get_reviews(db)


@router.delete('/{id}')
def delete_review(id: int, db: Session = Depends(get_db), current_user: UserDisplay = Depends(get_current_user)):
    review = db.query(DbReview).filter(DbReview.id == id, DbReview.user_id == current_user.id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found or you are not authorized to delete")
    return db_review.delete_review(db, id)
