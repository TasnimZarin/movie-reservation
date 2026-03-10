from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.showtime import Showtime
from app.schemas.showtime import ShowtimeCreate, ShowtimeResponse
from app.utils import get_current_user

router = APIRouter(prefix="/showtimes", tags=["Showtimes"])

@router.get("/", response_model=list[ShowtimeResponse])
def get_showtimes(db: Session = Depends(get_db)):
    return db.query(Showtime).all()

@router.post("/", response_model=ShowtimeResponse)
def create_showtime(showtime: ShowtimeCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    new_showtime = Showtime(**showtime.model_dump())
    db.add(new_showtime)
    db.commit()
    db.refresh(new_showtime)
    return new_showtime