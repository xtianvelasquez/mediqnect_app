from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schedule
class Schedule_Base(BaseModel):
  user_id: int
  intake_id: int
  scheduled_datetime: datetime

class Schedule_Create(Schedule_Base):
  status_id: int

class Schedule_Read(Schedule_Base):
  schedule_id: int
  medicine_name: str
  color_name: str

  class Config:
    from_attributes = True

class Schedule_Delete(BaseModel):
  intake_id: int
  schedule_id: int
