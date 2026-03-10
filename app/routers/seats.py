from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.seat import Seat
from app.models.booking import Booking
from app.schemas.seat import SeatResponse

router = APIRouter(prefix="/showtimes", tags=["Seats"])

@router.get("/{showtime_id}/seats")
def get_seats(showtime_id: int, db: Session = Depends(get_db)):
    seats = db.query(Seat).all()
    booked_seat_ids = {b.seat_id for b in db.query(Booking).filter(Booking.showtime_id == showtime_id).all()}
    result = []
    for seat in seats:
        result.append({
            "id": seat.id,
            "seat_number": seat.seat_number,
            "row": seat.row,
            "status": "booked" if seat.id in booked_seat_ids else "available"
        })
    return result