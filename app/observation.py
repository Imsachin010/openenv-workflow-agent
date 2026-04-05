from pydantic import BaseModel
from typing import List, Dict
from .state import Email, Task, CalendarEvent


class Observation(BaseModel):
    emails: List[Email]
    tasks: List[Task]
    calendar: List[CalendarEvent]
    history: List[Dict]
    timestep: int