from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

# Token
class Token_Base(BaseModel):
  token_hash: str
  is_active: bool
  issued_at: Optional[datetime] = None
  expires_at: Optional[datetime] = None
  revoked_at: Optional[datetime] = None
  user_id: Optional[int] = None

class Token_Response(BaseModel):
  access_token: str
  token_type: Literal['Bearer']
