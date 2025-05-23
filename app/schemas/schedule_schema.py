from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schedule Schemas
class Schedule_Base(BaseModel):
  scheduled_datetime: datetime
  prescription_id: int
  user_id: int
  status_id: Optional[int]

class Schedule_Create(Schedule_Base):
  pass

class Schedule_Read(Schedule_Base):
  schedule_id: int

  class Config:
    from_attributes = True
