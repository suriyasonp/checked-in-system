from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Event Schemas

class EventCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None

class EventResponse(EventCreate):
    id: int

    class Config:
        orm_mode = True

# Audience Schemas
class AudienceCreate(BaseModel):
    full_name_th: str
    full_name_en: Optional[str] = None
    nick_name_th: Optional[str] = None
    nick_name_en: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    organization: Optional[str] = None
    occupation: Optional[str] = None
    year_grade: Optional[int] = 0
    faculty: Optional[str] = None
    department: Optional[str] = None
    event_id: Optional[int] = None

class AudienceResponse(AudienceCreate):
    id: int

    class Config:
        orm_mode = True

# CheckIn Schemas
class CheckInCreate(BaseModel):
    audience_id: int
    event_id: int

class EventBase(BaseModel):
    name: str
    description: Optional[str]
    location: Optional[str]

class AudienceBase(BaseModel):
    full_name_th: str
    full_name_en: Optional[str]
    nick_name_th: Optional[str]
    nick_name_en: Optional[str]
    organization: Optional[str]
    faculty: Optional[str]
    department: Optional[str]

class CheckInResponse(BaseModel):
    check_in_time: datetime
    event: EventBase
    audience: AudienceBase

    class Config:
        orm_mode = True