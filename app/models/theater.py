from sqlalchemy import Column, Integer, String
from app.database import Base

class Theater(Base):
    __tablename__ = "theaters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    total_seats = Column(Integer, nullable=False)