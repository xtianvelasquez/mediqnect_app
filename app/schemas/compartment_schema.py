from pydantic import BaseModel

# Compartment
class Compartment_Base(BaseModel):
  compartment_name: str
  compartment_status_id: int

class Compartment_Create(Compartment_Base):
  compartment_set_id: int

class Compartment_Read(Compartment_Base):
  compartment_id: int

  class Config:
    from_attributes = True
