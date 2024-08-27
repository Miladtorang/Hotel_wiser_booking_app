from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship


class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    reservations = relationship("DbBooking", cascade="all,delete", back_populates="user")
    reviews = relationship("DbReview", back_populates="user")


class DbHotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    location = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    room_count = Column(Integer, nullable=False)

    rooms = relationship("Room", back_populates="hotel")
    reviews = relationship("DbReview", back_populates="hotel")
    reservations = relationship("DbBooking", back_populates="hotel")


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    room_type = Column(String)
    availability = Column(Boolean, default=True)

    hotel = relationship("DbHotel", back_populates="rooms")


class DbBooking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    hotel_id = Column(Integer, ForeignKey('hotels.id'), nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    user = relationship("DbUser", back_populates="reservations")
    hotel = relationship("DbHotel", back_populates="reservations")


class DbReview(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)

    user = relationship("DbUser", back_populates="reviews")
    hotel = relationship("DbHotel", back_populates="reviews")
