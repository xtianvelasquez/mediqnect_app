from pydantic import BaseModel, model_validator
from datetime import date, datetime
from zoneinfo import ZoneInfo
from app.services import convert_to_datetime

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

  @model_validator(mode='before')
  def check_timezone(cls, values):
    start = values.get('start_datetime')
    end = convert_to_datetime(values.get('end_date'))
    
    if start.tzinfo is None:
      raise ValueError('start_date is required.')
    if start.tzinfo.utcoffset(start) is None:
      start = start.replace(tzinfo=ZoneInfo('UTC'))

    values['start_datetime'] = start.astimezone(ZoneInfo('UTC'))
    values['end_date'] = end

    return values

class Intake_Create(Intake_Base):
  user_id: int
  status_id: int

class Intake_Read(Intake_Base):
  intake_id: int
  user_id: int
  is_scheduled: bool
  created_at: datetime
  modified_at: datetime
  status_name: str

  class Config:
    from_attributes = True
