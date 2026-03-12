from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    theater_id = Column(Integer, ForeignKey("theaters.id"), nullable=False)
    seat_number = Column(String, nullable=False)
    row = Column(String, nullable=False)

    theater = relationship("Theater")