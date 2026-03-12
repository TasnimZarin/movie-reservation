from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieResponse
from app.utils import get_current_user

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/", response_model=list[MovieResponse])
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()

@router.post("/", response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    new_movie = Movie(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie