from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Intake History
class Intake_History_Base(BaseModel):
  schedule_id: int

class Intake_History_Read(Intake_History_Base):
  scheduled_datetime: datetime
  history_id: int
  history_datetime: Optional[datetime] = None
  medicine_name: str
  status_name: str

  class Config:
    from_attributes = True

class Intake_History_Update(Intake_History_Base):
  history_datetime: datetime
  history_id: int

# Alarm
class Alarm_Confirm(Intake_History_Base):
  user_id: int
  intake_id: int
  history_datetime: datetime
