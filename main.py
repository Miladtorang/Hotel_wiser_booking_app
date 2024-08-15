from fastapi import FastAPI
from db.database import engine, Base
from router import user, hotel,booking
app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(user.router)
app.include_router(hotel.router)
app.include_router(booking.router)