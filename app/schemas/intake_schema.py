from pydantic import BaseModel, model_validator
from datetime import datetime
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
  end_datetime: datetime
  hour_interval: int
  dose: int
  component_id: int

  @model_validator(mode='before')
  def check_timezone(cls, values):
    start = convert_to_datetime(values.get('start_datetime'))
    end = convert_to_datetime(values.get('end_datetime'))

    if isinstance(start, str):
      start = datetime.fromisoformat(start.replace('Z', '+00:00'))

    if isinstance(end, str):
      end = datetime.fromisoformat(end.replace('Z', '+00:00'))

    if start.tzinfo is None or start.tzinfo.utcoffset(start) is None:
      start = start.replace(tzinfo=ZoneInfo('UTC'))

    if end.tzinfo is None or end.tzinfo.utcoffset(end) is None:
      end = end.replace(tzinfo=ZoneInfo('UTC'))

    values['start_datetime'] = start.astimezone(ZoneInfo('UTC'))
    values['end_datetime'] = end.astimezone(ZoneInfo('UTC'))

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
