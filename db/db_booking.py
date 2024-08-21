from sqlalchemy.orm import Session
from db.models import Booking, Hotel
from schemas import BookingBase
from fastapi import HTTPException


def create_reservation(db: Session, user_id: int, hotel_id: int, start_date: str, end_date: str):
    db_booking = Booking(
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
    return db.query(Booking).filter(Booking.user_id == user_id).all()


def cancel_reservation(db: Session, booking_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"detail": "Booking canceled"}
