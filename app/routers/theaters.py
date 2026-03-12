from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.theater import Theater
from app.models.seat import Seat
from app.schemas.theater import TheaterCreate, TheaterResponse
from app.utils import get_current_user

router = APIRouter(prefix="/theaters", tags=["Theaters"])

@router.get("/", response_model=list[TheaterResponse])
def get_theaters(db: Session = Depends(get_db)):
    return db.query(Theater).all()

@router.post("/", response_model=TheaterResponse)
def create_theater(theater: TheaterCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    new_theater = Theater(**theater.model_dump())
    db.add(new_theater)
    db.commit()
    db.refresh(new_theater)
    for i in range(1, theater.total_seats + 1):
        seat = Seat(theater_id=new_theater.id, seat_number=str(i), row="A")
        db.add(seat)
    db.commit()
    return new_theater