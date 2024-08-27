from sqlalchemy.orm import Session
from db.models import DbReview
from schemas import ReviewBase


def create_review(db: Session, request: ReviewBase, user_id: int):
    new_review = DbReview(
        user_id=user_id,
        hotel_id=request.hotel_id,
        rating=request.rating,
        comment=request.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


def get_reviews(db: Session):
    return db.query(DbReview).all()
