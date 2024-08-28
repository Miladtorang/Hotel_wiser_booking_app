from sqlalchemy.orm import Session
from db.models import DbBooking, DbHotel
from schemas import BookingBase
from fastapi import HTTPException


def create_reservation(db: Session, user_id: int, hotel_id: int, start_date: str, end_date: str):
    db_booking = DbBooking(
        user_id=user_id,
        hotel_id=hotel_id,
        start_date=start_date,
        end_date=end_date
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_all_bookings(db: Session, user_id: int):
    return db.query(DbBooking).filter(DbBooking.user_id == user_id).all()


def cancel_reservation(db: Session, booking_id: int):
    booking = db.query(DbBooking).filter(DbBooking.id == booking_id).first()
    db.delete(booking)
    db.commit()
    return 
