from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Intake History
class Intake_History_Base(BaseModel):
  user_id: int
  schedule_id: int
  intake_datetime: datetime
  status_id: Optional[int]

class Intake_History_Create(Intake_History_Base):
  pass

class Intake_History_Read(Intake_History_Base):
  history_id: int

  class Config:
    from_attributes = True
