from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.hash import bcrypt
import jwt, re
from zoneinfo import ZoneInfo

from app.config import secret_key
from app.database.session import get_db
from app.models import Token

Oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def create_token(data: dict):
  expires_at = datetime.now(ZoneInfo('UTC')) + timedelta(days=29)  # Token expires in 29 days
  issued_at = datetime.now(ZoneInfo('UTC'))

  data.update({'iat': issued_at, 'exp': expires_at})

  return jwt.encode(data, secret_key, algorithm='HS256')

def decode_token(token: str):
  try:
    return jwt.decode(token, secret_key, algorithms=['HS256'])
  
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=401, detail='Token has expired.')
  
  except jwt.DecodeError:
    raise HTTPException(status_code=401, detail='Invalid signature.')
  
  except jwt.InvalidTokenError:
    raise HTTPException(status_code=401, detail='Invalid token.')

def verify_token(db: Session = Depends(get_db), raw_token: str = Depends(Oauth2_scheme)):
  try:
    payload = decode_token(raw_token)
    user_id: int = payload.get('id')

    if user_id is None:
      raise HTTPException(status_code=401, detail='Invalid token.')

    stored_token = db.query(Token).filter(Token.token_hash == raw_token, Token.is_active == True, Token.user_id == user_id).first()

    if not stored_token:
      raise HTTPException(status_code=401, detail='Token not found or revoked.')

    return {'raw': raw_token, 'payload': payload}

  except Exception as e:
    raise HTTPException(status_code=500, detail='Unexpected error.')

def verify_ws_token(db: Session, raw_token: str):
  try:
    payload = decode_token(raw_token)
    user_id: int = payload.get('id')

    if user_id is None:
      raise HTTPException(status_code=401, detail='Invalid token.')

    stored_token = db.query(Token).filter(Token.token_hash == raw_token, Token.is_active == True, Token.user_id == user_id).first()

    if not stored_token:
      raise HTTPException(status_code=401, detail='Token not found or revoked.')

    return {'raw': raw_token, 'payload': payload}
  
  except Exception as e:
    raise HTTPException(status_code=500, detail='Unexpected error.')

def validate_password(password: str):
  pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$'
  return bool(re.match(pattern, password))

def hash_password(password: str):
  return bcrypt.hash(password)

def verify_password(plain_password: str, hashed_password: str):
  return bool(bcrypt.verify(plain_password, hashed_password))
