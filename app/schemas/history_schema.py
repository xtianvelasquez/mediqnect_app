from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from zoneinfo import ZoneInfo

# Intake History
class Intake_History_Base(BaseModel):
  schedule_id: int

class Intake_History_Create(Intake_History_Base):
  status_id: int

class Intake_History_Read(Intake_History_Base):
  scheduled_datetime: datetime
  history_id: int
  history_datetime: datetime
  medicine_name: str
  status_name: str

  class Config:
    from_attributes = True

class Intake_History_Update(Intake_History_Base):
  history_datetime: datetime = Field(..., description='Must be provided and timezone-aware.')
  history_id: int

  @model_validator(mode='before')
  def check_timezone(cls, values):
    history_dt = values.get('history_datetime')

    if isinstance(history_dt, str):
      history_dt = datetime.fromisoformat(history_dt.replace('Z', '+00:00'))

    if history_dt is not None:
      if history_dt.tzinfo is None or history_dt.tzinfo.utcoffset(history_dt) is None:
        history_dt = history_dt.replace(tzinfo=ZoneInfo('UTC'))
      values['start_datetime'] = history_dt.astimezone(ZoneInfo('UTC'))

    return values
