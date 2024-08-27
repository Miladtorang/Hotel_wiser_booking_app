from sqlalchemy.orm import Session
from db.models import DbHotel
from schemas import HotelBase


def create_hotel(db: Session, hotel: HotelBase):
    db_hotel = DbHotel(**hotel.dict())
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel


def get_all_hotels(db: Session):
    return db.query(DbHotel).all()


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
