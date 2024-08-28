from sqlalchemy.orm import Session
from db.models import DbReview
from schemas import ReviewBase, UserDisplay


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


def delete_review(db: Session, review_id: int):
    review = db.query(DbReview).filter(DbReview.id == review_id).first()
    db.delete(review)
    db.commit()
    return 
