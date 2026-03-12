from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, movies, theaters, seats, showtimes, bookings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Reservation System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://movie-reservation-five.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(theaters.router)
app.include_router(seats.router)
app.include_router(showtimes.router)
app.include_router(bookings.router)

@app.get("/")
def root():
    return {"message": "Movie Reservation API is running"}