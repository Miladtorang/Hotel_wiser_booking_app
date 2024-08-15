from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import BookingBase, BookingDisplay
from db.database import get_db
from db import db_booking

router = APIRouter(
    prefix='/bookings',
    tags=['bookings']
)


@router.post('/', response_model=BookingDisplay)
def create_new_booking(request: BookingBase, db: Session = Depends(get_db)):
    user_id = request.user_id
    return db_booking.create_reservation(db, request, user_id)


@router.get('/', response_model=List[BookingDisplay])
def list_bookings(db: Session = Depends(get_db)):
    user_id = 1
    return  db_booking.get_reservations(db, user_id)


@router.delete('/{id}', response_model=dict)
def cancel_booking(id: int, db: Session = Depends(get_db)):
    return  db_booking.cancel_reservation(db, id)
