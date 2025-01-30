from pydantic import BaseModel
from datetime import time as timeout

class CalendarAddSchema(BaseModel):
    day_name: str
    time: timeout
    description: str


class CalendarUpdateSchema(BaseModel):
    day_name: str | None = None
    time: timeout | None = None
    description: str | None = None