from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Prescription Schemas
class Prescription_Base(BaseModel):
  medicine_id: int
  intake_id: int
  user_id: int

class Prescription_Create(Prescription_Base):
  status_id: Optional[int]

class Prescription_Read(Prescription_Base):
  prescription_id: int
  created_at: datetime
  modified_at: datetime

  class Config:
    from_attributes = True
