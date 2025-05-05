from pydantic import BaseModel
from datetime import date, time

# Intake Schemas
class Intake_History_Base(BaseModel):
  intake_time: time
  intake_date: date
  intake_status_id: int

class Intake_History_Create(Intake_History_Base):
  schedule_id: int

class Intake_History_Read(Intake_History_Base):
  history_id: int

  class Config:
    from_attributes = True
