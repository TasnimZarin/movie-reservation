from pydantic import BaseModel

class SeatResponse(BaseModel):
    id: int
    theater_id: int
    seat_number: str
    row: str

    class Config:
        from_attributes = True