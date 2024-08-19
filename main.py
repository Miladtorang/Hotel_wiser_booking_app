from fastapi import FastAPI
from db.database import engine, Base
from router import user, hotel, booking, review
from auth import authentication

app = FastAPI()

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(hotel.router)
app.include_router(booking.router)
app.include_router(review.router)

Base.metadata.create_all(bind=engine)
