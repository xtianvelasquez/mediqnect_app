from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from zoneinfo import ZoneInfo

# Intake
class Component_Base(BaseModel):
  component_id: int
  component_name: str

class Color_Base(BaseModel):
  color_name: str

  class Config:
    from_attributes = True

class Intake_Base(BaseModel):
  start_datetime: datetime = Field(..., description='Must be provided and timezone-aware.')
  end_datetime: datetime = Field(..., description='Must be provided and timezone-aware.')
  hour_interval: int
  dose: int
  component_id: int

  @model_validator(mode='before')
  def check_timezone(cls, values):
    start = values.get('start_datetime')
    end = values.get('end_datetime')

    if isinstance(start, str):
      start = datetime.fromisoformat(start.replace('Z', '+00:00'))

    if isinstance(end, str):
      end = datetime.fromisoformat(end.replace('Z', '+00:00'))

    if start is not None:
      if start.tzinfo is None or start.tzinfo.utcoffset(start) is None:
        start = start.replace(tzinfo=ZoneInfo('UTC'))
      values['start_datetime'] = start.astimezone(ZoneInfo('UTC'))

    if start is not None:
      if end.tzinfo is None or end.tzinfo.utcoffset(end) is None:
        end = end.replace(tzinfo=ZoneInfo('UTC'))
      values['end_datetime'] = end.astimezone(ZoneInfo('UTC'))

    return values

class Intake_Read(BaseModel):
  user_id: int
  intake_id: int
  start_datetime: datetime
  end_datetime: datetime
  medicine_id: int
  medicine_name: str
  color_name: str
  status_name: str

  class Config:
    from_attributes = True
