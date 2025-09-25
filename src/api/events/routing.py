from fastapi import APIRouter
from .schemas import (
  EventSchema,
  EventListSchema,
  EventCreateSchema,
  EventUpdateSchema
)
router = APIRouter()


@router.get("/")
def read_events() -> EventListSchema:
  return {
    "results": [{"id": 1 }, {"id": 2 }, {"id": 3 }],
    "count": 3
  }

@router.post("/")
def create_events(payload: EventCreateSchema) -> EventSchema:
  data = payload.model_dump() #payload -> dict -> pydantic
  return {
    "id": 123, **data
  }


@router.get("/{event_id}")
def read_event(event_id:str) -> EventSchema:
  return {
    "id": event_id
  }

@router.put("/{event_id}")
def update_event(event_id:int, payload:EventUpdateSchema) -> EventSchema:
  data = payload.model_dump()
  return {
    "id": event_id, **data
  }

@router.delete("/{event_id}")
def delete_event(event_id:int, payload:dict={}) -> EventSchema:
  return {
    "id": event_id
  }