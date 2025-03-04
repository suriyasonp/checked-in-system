from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models, schemas, crud

# Initialize DB
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Event Routes
@app.post("/events/", response_model=schemas.EventResponse)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db, event)

@app.get("/events/", response_model=list[schemas.EventResponse])
def get_events(db: Session = Depends(get_db)):
    return crud.get_events(db)

# Audience Routes
@app.post("/audience/", response_model=schemas.AudienceResponse)
def register_audience(audience: schemas.AudienceCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Audience).filter(models.Audience.full_name_th == audience.full_name_th).first()
    if existing:
        raise HTTPException(status_code=400, detail="Audience already registered")
    return crud.create_audience(db, audience)

@app.get("/audience/{audience_id}", response_model=schemas.AudienceResponse)
def get_audience(audience_id: int, db: Session = Depends(get_db)):
    audience = crud.get_audience_by_id(db, audience_id)
    if not audience:
        raise HTTPException(status_code=404, detail="Audience not found")
    return audience

@app.get("/audience/event/{event_id}", response_model=list[schemas.AudienceResponse])
def get_audience_by_event(event_id: int, db: Session = Depends(get_db)):
    return crud.get_audience_by_eventid(db, event_id)

@app.get("/audience/name/{full_name}", response_model=schemas.AudienceResponse)
def get_audience_by_fullname(full_name: str, db: Session = Depends(get_db)):
    audience = crud.get_audience_by_fullname(db, full_name)
    if not audience:
        raise HTTPException(status_code=404, detail="Audience not found")
    return audience

# Check-in Routes
@app.post("/checkin/", response_model=schemas.CheckInResponse)
def check_in_user(checkin: schemas.CheckInCreate, db: Session = Depends(get_db)):
    result = crud.create_checkin(db, checkin)
    if result is None:
        raise HTTPException(status_code=404, detail="Invalid audience or event ID")
    
    return result

@app.get("/checkin/event/{event_id}", response_model=list[schemas.CheckInResponse])
def get_checkins_by_event_id(event_id: int, db: Session = Depends(get_db)):
    return crud.get_checkins_by_event_id(db, event_id)