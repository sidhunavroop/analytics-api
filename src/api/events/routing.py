import os
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from api.db.session import get_session
from .models import (
  EventModel,
  EventListSchema,
  EventCreateSchema,
  EventUpdateSchema,
  get_utc_now
)
router = APIRouter()
from api.db.config import DATABASE_URL


@router.get("/", response_model=EventListSchema)
def read_events(session: Session = Depends(get_session)):
  print(os.environ.get("DATABASE_URL"), DATABASE_URL)
  query = select(EventModel).order_by(EventModel.id.desc()).limit(10)
  results = session.exec(query).all()
  return {
    "results": results,
    "count": len(results)
  }

@router.post("/", response_model=EventModel)
def create_events(
    payload: EventCreateSchema,
    session: Session = Depends(get_session)):
  data = payload.model_dump() #payload -> dict -> pydantic
  
  obj = EventModel.model_validate(data)
  session.add(obj)
  session.commit()
  session.refresh(obj)
  return obj


@router.get("/{event_id}", response_model=EventModel)
def read_event(event_id:int, session: Session = Depends(get_session)):
  query = select(EventModel).where(EventModel.id == event_id)
  result = session.exec(query).first()
  if not result:
    raise HTTPException(status_code=404, detail="Event not found")
  return result

@router.put("/{event_id}", response_model=EventModel)
def update_event(event_id:int, payload:EventUpdateSchema, session: Session = Depends(get_session)):
  query = select(EventModel).where(EventModel.id == event_id)
  obj = session.exec(query).first()
  if not obj:
    raise HTTPException(status_code=404, detail="Event not found")
  
  data = payload.model_dump()
  for k, v in data.items():
    setattr(obj, k, v)
  obj.updated_at = get_utc_now()
  session.add(obj)
  session.commit()
  session.refresh(obj)
  return obj

@router.delete("/{event_id}")
def delete_event(event_id:int, payload:dict={}) -> EventModel:
  return {
    "id": event_id
  }