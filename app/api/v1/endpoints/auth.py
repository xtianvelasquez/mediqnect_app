from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.core import create_token, verify_token, validate_password
from app.services import inspect_duration
from app.models import User
from app.schemas import Token_Response, User_Login, User_Create, Change_Password

router = APIRouter()

@router.post('/token', response_model=Token_Response, status_code=200) # User login
async def user_login(data: User_Login, db: Session = Depends(get_db)):
  user = db.query(User).filter(
    User.username == data.username,
    User.user_password == data.user_password).first()
  
  if not user or user.user_password != data.user_password:
    raise HTTPException(status_code=401, detail='Invalid username or password.')

  token = create_token({
    'id': user.user_id,
    'sub': user.username
  })
  
  return {'access_token': token, 'token_type': 'bearer'}

@router.post('/signup', response_model=User_Create, status_code=200)
async def user_signup(data: User_Create, db: Session = Depends(get_db)):
  existing_user = db.query(User).filter(User.username == data.username).first()

  if existing_user:
    raise HTTPException(status_code=400, detail='Username already exists.')
  
  if not validate_password(data.user_password):
    raise HTTPException(status_code=400, detail='Password must be at least 6 characters long and include uppercase, lowercase, numbers, and special characters.')

  new_user = User(
    username=data.username,
    user_password=data.user_password,
    dispenser_code=data.dispenser_code
  )

  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  return new_user

@router.post('/username', status_code=200)
async def change_username(
  data: User_Login,
  token_payload = Depends(verify_token), 
  db: Session = Depends(get_db)):

  user = db.query(User).filter(User.user_id == token_payload['id']).first()
  existing_username = db.query(User).filter(User.username == data.username).first()
  
  if not user:
    raise HTTPException(status_code=404, detail='User not found.')

  if inspect_duration(datetime.utcnow(), user.date_modified, 7):
    raise HTTPException(status_code=403, detail='Username can only be changed after 7 days.')
  
  if user.user_password != data.user_password:
    raise HTTPException(status_code=403, detail='Incorrect password.')
  
  if existing_username:
    raise HTTPException(status_code=400, detail='Username already exists.')

  user.username = data.username
  db.commit()
  return {'message': 'Username updated successfully'}

@router.post('/password', status_code=200)
async def change_passsword(
  data: Change_Password,
  token_payload = Depends(verify_token),
  db: Session = Depends(get_db)):

  user = db.query(User).filter(User.user_id == token_payload['id']).first()

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
  if inspect_duration(datetime.utcnow(), user.date_modified, 7):
    raise HTTPException(status_code=403, detail='Password can only be changed after 7 days.')
  
  if user.user_password != data.current_password:
    raise HTTPException(status_code=403, detail='Incorrect password.')
  
  if not validate_password(data.new_password):
    raise HTTPException(status_code=400, detail='Password must be at least 6 characters long and include uppercase, lowercase, numbers, and special characters.')
  
  user.user_password = data.new_password
  db.commit()
  return {'message': 'Password updated successfully'}
