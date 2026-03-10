from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.booking import Booking
from app.models.seat import Seat
from app.schemas.booking import BookingCreate, BookingResponse
from app.utils import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    seat = db.query(Seat).filter(Seat.id == booking.seat_id).with_for_update().first()
    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")
    existing = db.query(Booking).filter(
        Booking.seat_id == booking.seat_id,
        Booking.showtime_id == booking.showtime_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Seat already booked")
    new_booking = Booking(
        user_id=current_user.id,
        showtime_id=booking.showtime_id,
        seat_id=booking.seat_id
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("/me", response_model=list[BookingResponse])
def my_bookings(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Booking).filter(Booking.user_id == current_user.id).all()

@router.delete("/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your booking")
    db.delete(booking)
    db.commit()
    return {"message": "Booking cancelled"}