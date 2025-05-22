from pydantic import BaseModel
from typing import Optional

# Compartment
class Compartment_Base(BaseModel):
  compartment_name: str
  status_name: Optional[str]

class Compartment_Create(Compartment_Base):
  set_id: int

class Compartment_Read(Compartment_Base):
  set_name: str
  compartment_id: int

  class Config:
    from_attributes = True
