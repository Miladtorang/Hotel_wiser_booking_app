from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.models import Booking, Room
from schemas import BookingBase as ReservationCreate


def create_reservation(db: Session, request: ReservationCreate, user_id: int):
    room = db.query(Room).filter(Room.id == request.room_id).first()
    if not room or not room.availability:
        raise HTTPException(status_code=400, detail="Room not available")
    new_reservation = Booking(
        user_id=user_id,
        room_id=request.room_id,
        start_date=request.start_date,
        end_date=request.end_date
    )
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    room.availability = False
    db.commit()

    return new_reservation


def get_reservations(db: Session, user_id: int):
    return db.query(Booking).filter(Booking.user_id == user_id).all()


def cancel_reservation(db: Session, reservation_id: int):
    reservation = db.query(Booking).filter(Booking.id == reservation_id).first()
    if reservation:
        db.delete(reservation)
        db.commit()
        return {"detail": "Reservation canceled"}
    else:
        raise HTTPException(status_code=404, detail="Reservation not found")
