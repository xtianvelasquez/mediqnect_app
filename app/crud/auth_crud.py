from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from app.core.security import hash_password
from app.models import User

def get_user(db: Session, user_id: int):
  try:
    return db.query(User).filter(User.user_id == user_id).first()

  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def get_all_user(db: Session, user_ids: List[int]):
  try:
    users = db.query(User).filter(User.user_id.in_(user_ids)).all()
  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e.orig)}')
  
  if not users:
    return []
  
  return [{'user_id': user.user_id, 'username': user.username} for user in users]

def get_username(db: Session, username: str):
  try:
    return db.query(User).filter(User.username == username).first() 
  
  except SQLAlchemyError as e:
      raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
  
  except Exception as e:
      raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def store_user(db: Session, username: str, password: str, dispenser_code: str):
  try:
    new_user = User(
      username=username,
      password_hash=hash_password(password),
      dispenser_code=dispenser_code
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if not new_user:
      raise HTTPException(status_code=500, detail='User could not be stored.')
    
    return {'message': 'Your account has been successfully created.'}
  
  except SQLAlchemyError as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
  
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def update_user_field(db: Session, user: str, field: str, value: str):
  try:
    setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return {'message': f'Your {field} has been changed successfully.'}

  except SQLAlchemyError as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')
