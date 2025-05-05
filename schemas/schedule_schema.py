from pydantic import BaseModel
from datetime import date, time

# Schedule Schemas
class Schedule_Base(BaseModel):
  scheduled_date: date
  scheduled_time: time
  schedule_status_id: int

class Schedule_Create(Schedule_Base):
  prescription_id: int

class Schedule_Read(Schedule_Base):
  schedule_id: int

  class Config:
    from_attributes = True
