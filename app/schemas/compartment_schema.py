from pydantic import BaseModel
from typing import Optional

# Compartment
class Compartment_Base(BaseModel):
  compartment_name: str
  status_id: Optional[int]

class Compartment_Create(Compartment_Base):
  set_id: int

class Compartment_Read(Compartment_Base):
  compartment_id: int
  set_name: str
  status_name: str

  class Config:
    from_attributes = True
