from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Intake History
class Intake_History_Base(BaseModel):
  user_id: int
  schedule_id: int
  scheduled_datetime: datetime

class Intake_History_Create(Intake_History_Base):
  status_id: int

class Intake_History_Read(Intake_History_Base):
  history_id: int
  history_datetime: datetime
  medicine_name: str
  status_name: str

  class Config:
    from_attributes = True
