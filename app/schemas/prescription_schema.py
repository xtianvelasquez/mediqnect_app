from pydantic import BaseModel
from datetime import datetime, date

# Prescription Schemas
class Prescription_Base(BaseModel):
  dose: int
  dose_component_id: int
  interval: int
  start_date: datetime
  end_date: date
  prescription_status_id: int

class Prescription_Create(Prescription_Base):
  medicine_id: int

class Prescription_Read(Prescription_Base):
  prescription_id: int
  date_created: datetime
  date_modified: datetime

  class Config:
    from_attributes = True
