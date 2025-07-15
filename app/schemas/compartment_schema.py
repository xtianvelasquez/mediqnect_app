from pydantic import BaseModel

# Compartment
class Compartment_Base(BaseModel):
  compartment_name: str

class Compartment_Create(Compartment_Base):
  set_id: int

class Compartment_Read(Compartment_Base):
  compartment_id: int
  status_name: str
  set_name: str

  class Config:
    from_attributes = True

class Clean_Compartment(BaseModel):
  compartment_id: int
