from sqlalchemy.orm import Session
import models, schemas

# Event CRUD
def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Events(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session):
    return db.query(models.Events).all()

# Audience CRUD
def create_audience(db: Session, audience: schemas.AudienceCreate):
    db_audience = models.Audience(**audience.dict())
    db.add(db_audience)
    db.commit()
    db.refresh(db_audience)
    return db_audience

def get_audience_by_id(db: Session, audience_id: int):
    return db.query(models.Audience).filter(models.Audience.id == audience_id).first()

def get_audience_by_eventid(db: Session, event_id: int):
    return db.query(models.Audience).join(models.Events).filter(models.Events.id == event_id).all()

def get_audience_by_fullname(db: Session, full_name: str):
    return db.query(models.Audience).filter(models.Audience.full_name_th == full_name).first()

def get_audience_not_checked_in(db: Session, event_id: int):
    subquery = db.query(models.CheckIn.audience_id).filter(models.CheckIn.event_id == event_id).subquery()
    return db.query(models.Audience).filter(~models.Audience.id.in_(subquery), models.Audience.event_id == event_id).all()

# CheckIn CRUD
def create_checkin(db: Session, checkin: schemas.CheckInCreate):
    db_audience = get_audience_by_id(db, checkin.audience_id)
    if not db_audience:
        return None  # Audience must exist

    db_event = db.query(models.Events).filter(models.Events.id == checkin.event_id).first()
    if not db_event:
        return None  # Event must exist

    db_checkin = models.CheckIn(audience_id=checkin.audience_id, event_id=checkin.event_id)
    db.add(db_checkin)
    db.commit()
    db.refresh(db_checkin)
    return db_checkin

def get_checkins_by_event_id(db: Session, event_id: int):
    return db.query(models.CheckIn) \
             .filter(models.CheckIn.event_id == event_id) \
             .order_by(models.CheckIn.check_in_time.asc()) \
             .join(models.Events) \
             .join(models.Audience) \
             .all()

