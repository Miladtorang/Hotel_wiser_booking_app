from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import HotelBase, HotelDisplay
from db.database import get_db
from db import db_hotels

router = APIRouter(
    prefix='/hotels',
    tags=['hotels']
)


@router.post('/', response_model=HotelDisplay)
def create_new_hotel(request: HotelBase, db: Session = Depends(get_db)):
    return db_hotels.create_hotel(db, request)


@router.get('/', response_model=List[HotelDisplay])
def list_hotels(db: Session = Depends(get_db), ):
    return db_hotels.get_all_hotels(db)


@router.get('/{id}', response_model=HotelDisplay)
def read_hotel(id: int, db: Session = Depends(get_db)):
    hotel = db_hotels.get_hotel(db, id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel


@router.put('/{id}', response_model=HotelDisplay)
def update_hotel(id: int, request: HotelBase, db: Session = Depends(get_db),):
    hotel = db_hotels.update_hotel(db, id, request)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel


@router.delete('/{id}', response_model=dict)
def delete_hotel(id: int, db: Session = Depends(get_db)):
    hotel = db_hotels.delete_hotel(db, id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return {"detail": "Hotel deleted"}
