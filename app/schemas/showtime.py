from pydantic import BaseModel
from datetime import datetime

class ShowtimeCreate(BaseModel):
    movie_id: int
    theater_id: int
    start_time: datetime
    end_time: datetime

class ShowtimeResponse(BaseModel):
    id: int
    movie_id: int
    theater_id: int
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True