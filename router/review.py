from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db_user import get_user_by_email
from schemas import ReviewBase, ReviewDisplay
from db. database import get_db
from db.db_review import create_review, get_reviews
from auth.oauth2 import oauth2_scheme

router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)


@router.post('/', response_model=ReviewDisplay)
def create_review(request: ReviewBase, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    user_id = get_user_by_email(db, payload.get("sub")).id
    return create_review(db, request, user_id)


@router.get('/', response_model=List[ReviewDisplay])
def list_reviews(db: Session = Depends(get_db)):
    return get_reviews(db)
