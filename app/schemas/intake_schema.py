from pydantic import BaseModel
from datetime import date, datetime

# Intake
class Component_Base(BaseModel):
  component_id: int
  component_name: str

class Color_Base(BaseModel):
  color_name: str

class Color_Read(Color_Base):
  color_id: int

  class Config:
    from_attributes = True

class Intake_Base(BaseModel):
  start_datetime: datetime
  end_date: date
  hour_interval: int
  dose: int
  component_id: int

class Intake_Create(Intake_Base):
  user_id: int
  status_id: int

class Intake_Read(Intake_Base):
  intake_id: int
  user_id: int
  created_at: datetime
  modified_at: datetime
  status_name: str

  class Config:
    from_attributes = True
