from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship


class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # Relationships
    reservations = relationship("Booking", back_populates="user")
    reviews = relationship("Review", back_populates="user")


class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    location = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    room_count = Column(Integer, nullable=False)

    # Relationships
    rooms = relationship("Room", back_populates="hotel")
    reviews = relationship("Review", back_populates="hotel")


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    room_type = Column(String)
    availability = Column(Boolean, default=True)

    # Relationships
    hotel = relationship("Hotel", back_populates="rooms")
    reservations = relationship("Booking", back_populates="room")


class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    # Relationships
    user = relationship("DbUser", back_populates="reservations")
    room = relationship("Room", back_populates="reservations")


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)

    # Relationships
    user = relationship("DbUser", back_populates="reviews")
    hotel = relationship("Hotel", back_populates="reviews")
