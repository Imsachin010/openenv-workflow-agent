from pydantic import BaseModel
from typing import Optional, Literal, Dict


ActionType = Literal[
    "classify",
    "reply",
    "schedule",
    "prioritize",
    "request_info",
    "archive"
]


class Action(BaseModel):
    type: ActionType
    target_id: str                  # email/task id
    payload: Optional[Dict] = None  # flexible for different actions