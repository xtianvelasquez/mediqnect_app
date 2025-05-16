from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.hash import bcrypt
import jwt, re

from app.core import secret_key

Oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def create_token(data: dict):
  expires_at = datetime.utcnow() + timedelta(days=29)  # Token expires in 29 days
  issued_at = datetime.utcnow()

  data.update({'iat': issued_at, 'exp': expires_at})

  return jwt.encode(data, secret_key, algorithm='HS256')

def decode_token(token: str):
  try:
    return jwt.decode(token, secret_key, algorithms=["HS256"])
  
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=401, detail="Token has expired.")
  
  except jwt.DecodeError:
    raise HTTPException(status_code=401, detail="Invalid signature.")
  
  except jwt.InvalidTokenError:
    raise HTTPException(status_code=401, detail="Invalid token.")

def verify_token(raw_token: str = Depends(Oauth2_scheme)):
  payload = decode_token(raw_token)
  return {'raw': raw_token, 'payload': payload}

def validate_password(password: str):
  pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$'
  return bool(re.match(pattern, password))

def hash_password(password: str):
  return bcrypt.hash(password)

def verify_password(plain_password: str, hashed_password: str):
  return bool(bcrypt.verify(plain_password, hashed_password))
