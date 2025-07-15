from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Intake
class Component_Base(BaseModel):
  component_id: int
  component_name: str

class Color_Base(BaseModel):
  color_name: str

  class Config:
    from_attributes = True

class Intake_Base(BaseModel):
  medicine_id: int
  start_datetime: datetime
  end_datetime: datetime
  hour_interval: int
  dose: int
  component_id: int

class Intake_Read(BaseModel):
  user_id: int
  intake_id: int
  start_datetime: datetime
  end_datetime: datetime
  medicine_id: int
  medicine_name: str
  net_content: Optional[int]
  expiration_date: Optional[datetime]
  color_name: str
  status_name: str
  compartment_name: str

  class Config:
    from_attributes = True

class Delete_Intake(BaseModel):
  intake_id: int
