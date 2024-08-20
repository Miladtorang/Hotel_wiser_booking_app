from sqlalchemy.orm import Session
from db.models import Booking, Hotel
from schemas import BookingBase
from fastapi import HTTPException


def create_reservation(db: Session, booking: BookingBase, user_id: int):
    hotel = db.query(Hotel).filter(Hotel.id == booking.hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="Room not found")

    db_booking = Booking(
        user_id=user_id,
        hotel_id=booking.hotel_id,
        start_date=booking.start_date,
        end_date=booking.end_date
    )

    db.add(db_booking)

    db.commit()

    db.refresh(db_booking)
    return db_booking


def cancel_reservation(db: Session, booking_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()

    return {"detail": "Booking canceled"}
