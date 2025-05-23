from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.core import create_token, verify_token, validate_password, verify_password, hash_password
from app.crud import store_token, logout_token, get_user, get_username, authenticate_user, store_user, update_user_field
from app.services import inspect_duration
from app.schemas import Token_Response, User_Auth, User_Read, User_Create, Change_Password

router = APIRouter()

@router.post('/token', response_model=Token_Response, status_code=200)
async def user_login(data: User_Auth, db: Session = Depends(get_db)):
  user = authenticate_user(db, data.username, data.password)

  token = create_token({'id': user.user_id, 'sub': user.username})
  stored_token = store_token(db, token)

  return {'access_token': stored_token, 'token_type': 'Bearer'}

@router.post('/signup', status_code=201)
async def user_signup(data: User_Create, db: Session = Depends(get_db)):
  existing_user = get_username(db, data.username)

  if existing_user:
    raise HTTPException(status_code=400, detail='Username already exists.')
  
  if not validate_password(data.password):
    raise HTTPException(status_code=400, detail='Password must be at least 6 characters long and include uppercase, lowercase, numbers, and special characters.')
  
  stored_user = store_user(db, data.username, data.password, data.dispenser_code)

  return stored_user

@router.post('/username', status_code=200)
async def change_username(
  data: User_Auth,
  token_payload = Depends(verify_token), 
  db: Session = Depends(get_db)):

  payload = token_payload['payload']
  user = get_user(db, payload['id'])
  existing_username = get_username(db, data.username)
  
  if not user:
    raise HTTPException(status_code=404, detail='User not found.')

  if inspect_duration(datetime.utcnow(), user.modified_at, 7):
    raise HTTPException(status_code=403, detail='Username can only be changed after 7 days.')

  if existing_username:
    raise HTTPException(status_code=400, detail='Username already exists.')
  
  if not verify_password(user.password_hash, data.password):
    raise HTTPException(status_code=403, detail='Incorrect password.')

  new_username = update_user_field(db, user, 'username', data.username)

  return new_username

@router.post('/password', status_code=200)
async def change_password(
  data: Change_Password,
  token_payload = Depends(verify_token),
  db: Session = Depends(get_db)):

  payload = token_payload['payload']
  user = get_user(db, payload['id'])

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')

  if inspect_duration(datetime.utcnow(), user.modified_at, 7):
    raise HTTPException(status_code=403, detail='Password can only be changed after 7 days.')
  
  if not verify_password(user.password_hash, data.password):
    raise HTTPException(status_code=403, detail='Incorrect password.')

  new_password = update_user_field(db, user, 'password_hash', hash_password(data.new_password))

  return new_password

@router.post('/logout', status_code=204)
async def logout(token_payload = Depends(verify_token), db: Session = Depends(get_db)):
  return logout_token(db, token_payload['raw'])

@router.get('/user', response_model=User_Read, status_code=200)
async def current_user(token_payload = Depends(verify_token), db: Session = Depends(get_db)):
  payload = token_payload['payload']
  user = get_user(db, payload['id'])

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
  return [{
    'user_id': user.user_id,
    'username': user.username,
    'created_at': user.created_at,
    'modified_at': user.modified_at
  }]

@router.get('/protected', status_code=200)
async def protected_route(token_payload: dict = Depends(verify_token)):
  payload = token_payload['payload']
  return {'message': f'Welcome, {payload['sub']}'}
