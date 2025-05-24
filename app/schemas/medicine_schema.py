from pydantic import BaseModel
from typing import Optional
from datetime import date

# Medicine
class Form_Base(BaseModel):
  form_id: int
  form_name: str

class Medicine_Base(BaseModel):
  medicine_name: str
  form_id: int
  net_content: Optional[int]
  expiration_date: Optional[date]
  status_id: Optional[int]

class Medicine_Create(Medicine_Base):
  pass

class Medicine_Read(Medicine_Base):
  medicine_id: int

  class Config:
    from_attributes = True

class Medicine_Compartment_Base(BaseModel):
  compartment_id: int

class Medicine_Compartment_Create(Medicine_Compartment_Base):
  medicine_id: int
  user_id: int

class Medicine_Compartment_Read(Medicine_Compartment_Create):
  medicine_compartment_id: int

  class Config:
    from_attributes = True
