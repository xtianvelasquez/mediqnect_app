from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class Component_Base(BaseModel):
  component_id: int
  component_name: str

# Intake Schemas
class Intake_Base(BaseModel):
  start_datetime: datetime
  end_date: date
  hour_interval: int
  dose: int
  component_id: int

class Intake_Create(Intake_Base):
  pass

class Intake_Read(Intake_Base):
  intake_id: int

  class Config:
    from_attributes = True
