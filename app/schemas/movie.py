from pydantic import BaseModel

class MovieCreate(BaseModel):
    title: str
    description: str
    duration_mins: int

class MovieResponse(BaseModel):
    id: int
    title: str
    description: str
    duration_mins: int

    class Config:
        from_attributes = True