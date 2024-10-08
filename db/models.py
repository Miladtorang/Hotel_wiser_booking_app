from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship


class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean)

    owned_hotels = relationship("DbHotel", cascade="all,delete", back_populates="owner")
    reservations = relationship("DbBooking", cascade="all,delete", back_populates="user")
    reviews = relationship("DbReview", cascade="all,delete", back_populates="user")


class DbHotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, index=True, nullable=False)
    location = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)

    owner = relationship("DbUser", back_populates="owned_hotels")
    reviews = relationship("DbReview", cascade="all,delete", back_populates="hotel")
    reservations = relationship("DbBooking", cascade="all,delete", back_populates="hotel")


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
