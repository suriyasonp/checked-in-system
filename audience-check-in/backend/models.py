from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, default=datetime.datetime.utcnow)
    location = Column(String)

class Audience(Base):
    __tablename__ = "audiences"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name_th = Column(String, unique=True, index=True, nullable=False)
    full_name_en = Column(String, unique=True, index=True, nullable=True)
    nick_name_th = Column(String, nullable=True)
    nick_name_en = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    organization = Column(String)
    occupation = Column(String)
    year_grade = Column(Integer, default=0)
    faculty = Column(String)
    department = Column(String)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)

class CheckIn(Base):
    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    audience_id = Column(Integer, ForeignKey("audiences.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    check_in_time = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    audience = relationship("Audience", backref="checkins")
    event = relationship("Events", backref="checkins")

    class Config:
        orm_mode = True