from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Intake Schemas
class Intake_History_Base(BaseModel):
  intake_datetime: datetime
  schedule_id: int
  user_id: int
  status_id: Optional[int]

class Intake_History_Create(Intake_History_Base):
  pass

class Intake_History_Read(Intake_History_Base):
  history_id: int

  class Config:
    from_attributes = True
