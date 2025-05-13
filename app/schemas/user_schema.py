from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class Token_Response(BaseModel):
  access_token: str
  token_type: Literal['bearer']

# User Schemas
class Change_Password(BaseModel):
  new_password: str
  current_password: str

class User_Base(BaseModel):
  username: str

class User_Create(User_Base):
  password: str
  dispenser_code: Optional[int]

class User_Login(User_Base):
  password: str

class User_Read(User_Base):
  user_id: int
  date_created: datetime
  date_modified: datetime

  class Config:
    from_attributes = True
