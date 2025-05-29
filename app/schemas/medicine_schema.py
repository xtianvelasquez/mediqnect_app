from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

# Medicine
class Form_Base(BaseModel):
  form_id: int
  form_name: str

class Medicine_Base(BaseModel):
  medicine_name: str
  form_id: int
  net_content: Optional[int] = None
  expiration_date: Optional[date] = None

class Medicine_Create(Medicine_Base):
  user_id: int
  status_id: int

class Medicine_Read(Medicine_Base):
  medicine_id: int
  user_id: int
  created_at: datetime
  modified_at: datetime
  status_name: str

  class Config:
    from_attributes = True

class Medicine_Compartment_Base(BaseModel):
  compartment_id: int

class Medicine_Compartment_Create(Medicine_Compartment_Base):
  user_id: int
  medicine_id: int

class Medicine_Compartment_Read(Medicine_Compartment_Create):
  medicine_compartment_id: int

  class Config:
    from_attributes = True
