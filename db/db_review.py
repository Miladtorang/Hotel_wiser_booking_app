from sqlalchemy import func
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

def update_review(db: Session, id: int, review: ReviewBase):
    db_review = db.query(DbReview).filter(DbReview.id == id).first()
    if not db_review:
        return None
    for key, value in review.dict().items():
        setattr(db_review, key, value)
    db.commit()
    db.refresh(db_review)
    return db_review

def calculate_hotel_rating(db: Session, hotel_id: int):
   reviews = db.query(DbReview).filter(DbReview.hotel_id == hotel_id).all()
   if not reviews:
       return 0
   average_rating = sum([review.rating for review in reviews]) / len(reviews)
   return average_rating


def delete_review(db: Session, review_id: int):
    review = db.query(DbReview).filter(DbReview.id == review_id).first()
    db.delete(review)
    db.commit()
    return 

