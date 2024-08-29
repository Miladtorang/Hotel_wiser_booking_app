from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from schemas import HotelBase, HotelDisplay,RatedHotelDisplay
from db.database import get_db
from db import db_hotels
from db.models import DbUser,DbHotel
from auth.oauth2 import get_current_user
from db.db_review import calculate_hotel_rating

router = APIRouter(
    prefix='/hotels',
    tags=['hotels']
)


@router.post('/', response_model=HotelDisplay, status_code=201)
def create_new_hotel(request: HotelBase, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    return db_hotels.create_hotel(db, request)


@router.get('/', response_model=List[HotelDisplay], status_code=200)
def list_hotels(
    location: Optional[str] = Query(None, description="Filter by hotel location"),
    name: Optional[str] = Query(None, description="Filter by hotel name"),
    min_price: Optional[int] = Query(None, description="Filter by minimum price"),
    max_price: Optional[int] = Query(None, description="Filter by maximum price"),
    db: Session = Depends(get_db)
):
    return db_hotels.get_all_hotels(db, location=location, name=name, min_price=min_price, max_price=max_price)


# def list_hotels(db: Session = Depends(get_db)):
#     return db_hotels.get_all_hotels(db)




@router.get('/{id}', response_model=RatedHotelDisplay, status_code=200)
def read_hotel(id: int, db: Session = Depends(get_db)):
    hotel = db_hotels.get_hotel(db, id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    average_rating = calculate_hotel_rating(db, id)
    return RatedHotelDisplay(
        id=hotel.id,
        name= hotel.name,
        user_id= hotel.user_id,
        location= hotel.location,
        description=hotel.description,
        price= hotel.price,
        rating= average_rating
    )


@router.put('/{id}', response_model=HotelDisplay, status_code=200)
def update_hotel(id: int, request: HotelBase, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    hotel = db.query(DbHotel).filter(DbHotel.id == id).first() 
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    if id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized")
    return db_hotels.update_hotel(db, id, request)


@router.delete('/{id}',status_code=204)
def delete_hotel(id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    hotel = db.query(DbHotel).filter(DbHotel.id == id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found ")
    if id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized")
    db_hotels.delete_hotel(db, id)
    return 



