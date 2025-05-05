from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

# Medicine Schemas
class Medicine_Base(BaseModel):
  medicine_name: str
  medicine_form_id: int
  net_content: Optional[int]
  expiration_date: Optional[date]
  medicine_status_id: int

class Medicine_Create(Medicine_Base):
  compartment_id: int
  user_id: int

class Medicine_Read(Medicine_Base):
  medicine_id: int
  date_created: datetime
  date_modified: datetime

  class Config:
    from_attributes = True
