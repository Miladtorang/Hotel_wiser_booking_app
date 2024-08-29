from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ReviewBase, ReviewDisplay, UserDisplay
from db.database import get_db
from db import db_review
from auth.oauth2 import get_current_user
from db.models import DbUser, DbReview, DbHotel

router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)


@router.post('/', response_model=ReviewDisplay, status_code=201)
def create_review_endpoint(request: ReviewBase, db: Session = Depends(get_db),
                           current_user: DbUser = Depends(get_current_user)):
    if request.user_id != current_user.id:
        raise HTTPException(400, 'You are not authorized')
    hotel = db.query(DbHotel).filter(DbHotel.id == request.hotel_id).first()
    if hotel.user_id == current_user.id:
        raise  HTTPException(status_code=400, detail="You can not review your own hotel" )
    existing_review = db.query(DbReview).filter(DbReview.user_id == current_user.id).filter(DbReview.hotel_id == request.hotel_id).first()
    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed the hotel" )
    if request.rating < 1 or 5 < request.rating:
        raise HTTPException(status_code=400, detail="Rate should be between 1 to 5" )

    return db_review.create_review(db, request, current_user.id)


@router.get('/', response_model=List[ReviewDisplay], status_code=200)
def list_reviews(db: Session = Depends(get_db)):
    return db_review.get_reviews(db)


@router.put('/{id}', response_model=ReviewDisplay, status_code=200)
def update_review(id: int, request: ReviewBase, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    review = db.query(DbReview).filter(DbReview.id == id).first() 
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized")
    return db_review.update_review(db, id, request)


@router.delete('/{id}',status_code=204)
def delete_review(id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    review = db.query(DbReview).filter(DbReview.id == id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized")
    db_review.delete_review(db, id)
    return

