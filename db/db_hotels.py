from typing import Optional
from sqlalchemy.orm import Session
from db.models import DbHotel
from schemas import HotelBase


def create_hotel(db: Session, request: HotelBase):
    new_hotel = DbHotel(
        name = request.name,
        user_id = request.user_id,
        location = request.location,
        description = request.description,
        price = request.price
    )
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return new_hotel


def get_all_hotels(
    db: Session, 
    location: Optional[str] = None, 
    name: Optional[str] = None, 
    min_price: Optional[int] = None, 
    max_price: Optional[int] = None
):
    query = db.query(DbHotel)
    
    if location:
        query = query.filter(DbHotel.location.ilike(f"%{location}%"))
    
    if name:
        query = query.filter(DbHotel.name.ilike(f"%{name}%"))
    
    if min_price is not None:
        query = query.filter(DbHotel.price >= min_price)
    
    if max_price is not None:
        query = query.filter(DbHotel.price <= max_price)
    
    return query.all()

# def get_all_hotels(db: Session):
#     return db.query(DbHotel).all()


def get_hotel(db: Session, id: int):
    return db.query(DbHotel).filter(DbHotel.id == id).first()




def update_hotel(db: Session, id: int, hotel: HotelBase):
    db_hotel = db.query(DbHotel).filter(DbHotel.id == id).first()
    if not db_hotel:
        return None
    for key, value in hotel.dict().items():
        setattr(db_hotel, key, value)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel


def delete_hotel(db: Session, id: int):
    db_hotel = db.query(DbHotel).filter(DbHotel.id == id).first()
    if not db_hotel:
        return None
    db.delete(db_hotel)
    db.commit()
    return db_hotel
