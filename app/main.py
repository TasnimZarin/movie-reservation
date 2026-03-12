from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import auth, movies, theaters, seats, showtimes, bookings

app = FastAPI(title="Movie Reservation System")

app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(theaters.router)
app.include_router(seats.router)
app.include_router(showtimes.router)
app.include_router(bookings.router)

@app.get("/")
def root():
    return {"message": "Movie Reservation API is running"}