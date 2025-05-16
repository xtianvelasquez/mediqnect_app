from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

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
  token_type: Literal['bearer']
