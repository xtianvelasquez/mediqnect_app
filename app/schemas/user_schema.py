from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
