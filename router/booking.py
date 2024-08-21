from typing import List
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.models import Booking, Hotel
from schemas import BookingBase, BookingDisplay, UserDisplay
from db.database import get_db
from db import db_booking
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/bookings',
    tags=['bookings']
)


@router.post('/', response_model=BookingDisplay)
def create_new_booking(request: BookingBase, db: Session = Depends(get_db),
                       current_user: UserDisplay = Depends(get_current_user)):
    if request.user_id is not current_user.id:
        raise HTTPException(403, 'Forbidden')

    hotel = db.query(Hotel).filter(Hotel.id == request.hotel_id).first()

    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    return db_booking.create_reservation(db, request.user_id, request.hotel_id, request.start_date, request.end_date)


@router.get('/', response_model=List[BookingDisplay])
def list_bookings(db: Session = Depends(get_db), current_user: UserDisplay = Depends(get_current_user)):
    return db_booking.get_all_bookings(db, current_user.id)


@router.delete('/{id}', response_model=dict)
def cancel_booking(id: int, db: Session = Depends(get_db), current_user: UserDisplay = Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == id, Booking.user_id == current_user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found or not authorized to cancel")
    return db_booking.cancel_reservation(db, id)
