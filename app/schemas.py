from typing import Annotated
from pydantic import BaseModel, Field
from datetime import time

class CalendarAddSchema(BaseModel):
    day_name: str
    time: time
    description: str