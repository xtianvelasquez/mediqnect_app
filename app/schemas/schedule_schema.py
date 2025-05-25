from pydantic import BaseModel
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
  status_name: str

  class Config:
    from_attributes = True
