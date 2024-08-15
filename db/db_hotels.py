from sqlalchemy.orm import Session
from db.models import Hotel
from schemas import HotelBase


def create_hotel(db: Session, hotel: HotelBase):
    db_hotel = Hotel(**hotel.dict())
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel


def get_all_hotels(db: Session):
    return db.query(Hotel).all()


def get_hotel(db: Session, id: int):
    return db.query(Hotel).filter(Hotel.id == id).first()


def update_hotel(db: Session, id: int, hotel: HotelBase):
    db_hotel = db.query(Hotel).filter(Hotel.id == id).first()
    if not db_hotel:
        return None
    for key, value in hotel.dict().items():
        setattr(db_hotel, key, value)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel


def delete_hotel(db: Session, id: int):
    db_hotel = db.query(Hotel).filter(Hotel.id == id).first()
    if not db_hotel:
        return None
    db.delete(db_hotel)
    db.commit()
    return db_hotel
