from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class Intake_Base(BaseModel):
  start_datetime: datetime
  end_date: date
  hour_interval: int
  dose: int
  dose_component_id: int
  status_id: Optional[int]

class Intake_Create(Intake_Base):
  pass

class Intake_Read(Intake_Base):
  intake_id: int

  class Config:
    from_attributes = True
