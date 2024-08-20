from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ReviewBase, ReviewDisplay
from db.database import get_db
from db.db_review import create_review, get_reviews
from auth.oauth2 import get_current_user
from db.models import DbUser

router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)


@router.post('/', response_model=ReviewDisplay)
def create_review_endpoint(request: ReviewBase, db: Session = Depends(get_db),
                           current_user: DbUser = Depends(get_current_user)):
    user_id = current_user.id
    return create_review(db, request, user_id)


@router.get('/', response_model=List[ReviewDisplay])
def list_reviews(db: Session = Depends(get_db)):
    return get_reviews(db)
