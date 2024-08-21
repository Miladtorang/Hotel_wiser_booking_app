from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserDisplay(BaseModel):
    id: int
    user_name: str
    email: EmailStr
    # role: str

    class Config:
        orm_mode = True


class HotelBase(BaseModel):
    name: str
    location: str
    description: Optional[str] = None
    room_count: int


class HotelDisplay(HotelBase):
    id: int

    class Config:
        from_attributes = True


class BookingBase(BaseModel):
    user_id: int
    hotel_id: int
    start_date: datetime
    end_date: datetime


class BookingDisplay(BookingBase):
    id: int
    user_id: int
    hotel_id: int
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True


class ReviewBase(BaseModel):
    hotel_id: int
    rating: int
    comment: Optional[str] = None


class ReviewDisplay(ReviewBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class TokenBase(BaseModel):
    username: str
    password: str
