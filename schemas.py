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
    room_id: int
    start_date: datetime
    end_date: datetime


class BookingDisplay(BookingBase):
    id: int

    class Config:
        from_attributes = True


class ReservationCreate(BaseModel):
    room_id: int
    start_date: datetime
    end_date: datetime


class ReservationDisplay(ReservationCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
