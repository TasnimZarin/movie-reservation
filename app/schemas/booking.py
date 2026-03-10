from pydantic import BaseModel

class BookingCreate(BaseModel):
    showtime_id: int
    seat_id: int

class BookingResponse(BaseModel):
    id: int
    user_id: int
    showtime_id: int
    seat_id: int
    status: str

    class Config:
        from_attributes = True