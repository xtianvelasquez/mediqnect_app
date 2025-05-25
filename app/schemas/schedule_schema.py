from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo

# Schedule
class Schedule_Base(BaseModel):
  user_id: int
  intake_id: int
  scheduled_datetime: datetime

  @validator('scheduled_datetime', pre=True, always=True)
  def check_timezone(cls, dt):
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
      raise ValueError('scheduled_datetime must be timezone-aware')

    return dt.astimezone(ZoneInfo('UTC'))

class Schedule_Create(Schedule_Base):
  status_id: int

class Schedule_Read(Schedule_Base):
  schedule_id: int
  status_name: str

  class Config:
    from_attributes = True
