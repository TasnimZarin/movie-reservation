from pydantic import BaseModel

class TheaterCreate(BaseModel):
    name: str
    total_seats: int

class TheaterResponse(BaseModel):
    id: int
    name: str
    total_seats: int

    class Config:
        from_attributes = True