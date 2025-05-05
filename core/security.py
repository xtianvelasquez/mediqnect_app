from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import jwt, re
from . import secret_key

Oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def create_token(data: dict):
  expires = datetime.utcnow() + timedelta(days=29)  # Token expires in 29 days
  data.update({'exp': expires})

  return jwt.encode(data, secret_key, algorithm='HS256')

def decode_token(token: str):
  try:
    return jwt.decode(token, secret_key, algorithms=['HS256'])

  except jwt.InvalidTokenError:
    print('Invalid token.')
    return None
  
  except jwt.ExpiredSignatureError:
    print('Expired signature.')
    return None
  
  except jwt.DecodeError:
    print('Invalid signatue.')
    return None

def verify_token(token: str = Depends(Oauth2_scheme)):
  return decode_token(token)

def validate_password(password: str):
  pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$'
  return bool(re.match(pattern, password))
