from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime, date

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

# User
class User_Base(BaseModel):
  username: str

class User_Create(User_Base):
  password: str
  dispenser_code: Optional[str]

class User_Read(User_Base):
  user_id: int
  created_at: datetime
  modified_at: datetime

  class Config:
    from_attributes = True

class User_Auth(User_Base):
  password: str

class Change_Password(User_Auth):
  new_password: str

# Token
class Token_Base(BaseModel):
  token_hash: str
  is_active: bool
  issued_at: Optional[datetime]
  expires_at: Optional[datetime]
  revoked_at: Optional[datetime]
  user_id: Optional[int]

class Token_Response(BaseModel):
  access_token: str
  token_type: Literal['Bearer']

# Medicine
class Form_Base(BaseModel):
  form_id: int
  form_name: str

class Medicine_Base(BaseModel):
  medicine_name: str
  form_id: int
  net_content: Optional[int]
  expiration_date: Optional[date]

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

# Intake
class Component_Base(BaseModel):
  component_id: int
  component_name: str

class Color_Base(BaseModel):
  color_name: str

class Color_Read(Color_Base):
  color_id: int

  class Config:
    from_attributes = True

class Intake_Base(BaseModel):
  start_datetime: datetime
  end_date: date
  hour_interval: int
  dose: int
  component_id: int

class Intake_Create(Intake_Base):
  user_id: int
  status_id: int

class Intake_Read(Intake_Base):
  intake_id: int
  user_id: int
  is_scheduled: bool
  created_at: datetime
  modified_at: datetime
  status_name: str

  class Config:
    from_attributes = True

# Schedule
class Schedule_Base(BaseModel):
  user_id: int
  intake_id: int
  scheduled_datetime: datetime

class Schedule_Create(Schedule_Base):
  status_id: int

class Schedule_Read(Schedule_Base):
  schedule_id: int
  status_name: str

  class Config:
    from_attributes = True

# Intake History
class Intake_History_Base(BaseModel):
  user_id: int
  schedule_id: int
  intake_datetime: datetime

class Intake_History_Create(Intake_History_Base):
  status_id: int

class Intake_History_Read(Intake_History_Base):
  history_id: int
  modified_at: datetime
  status_name: str

  class Config:
    from_attributes = True
