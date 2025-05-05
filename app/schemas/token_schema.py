from pydantic import BaseModel
from typing import Literal

# Token
class Token_Response(BaseModel):
  access_token: str
  token_type: Literal['bearer']
