from pydantic import BaseModel
from typing import Optional

# Compartment
class Compartment_Base(BaseModel):
  compartment_name: str
  status_id: Optional[int]

class Compartment_Create(Compartment_Base):
  set_id: int

class Compartment_Read(Compartment_Base):
  status_name: str
  set_name: str
  compartment_id: int

  class Config:
    from_attributes = True
