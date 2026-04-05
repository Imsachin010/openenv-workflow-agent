from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum


class EmailPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Email(BaseModel):
    id: str
    sender: str
    subject: str
    body: str


class HiddenEmailState(BaseModel):
    email_id: str
    true_intent: str               # e.g., "meeting_request", "spam", "task"
    urgency: EmailPriority
    requires_response: bool
    deadline: Optional[int]        # timestep deadline
    missing_information: bool      # does agent need to ask clarification?


class Task(BaseModel):
    id: str
    description: str
    completed: bool = False
    deadline: Optional[int]


class CalendarEvent(BaseModel):
    id: str
    title: str
    time: int


class EnvironmentState(BaseModel):
    # Observed components
    emails: List[Email]
    tasks: List[Task]
    calendar: List[CalendarEvent]
    history: List[Dict] = Field(default_factory=list)

    # Hidden components (NOT exposed to agent)
    hidden_email_states: List[HiddenEmailState]

    # Global timestep
    timestep: int = 0

    # Episode termination
    done: bool = False