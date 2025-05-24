from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import User
from app.core.security import hash_password, verify_password

def get_user(db: Session, _id: int):
  try:
    return db.query(User).filter(User.user_id == _id).first()

  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def get_username(db: Session, username: str):
  try:
    return db.query(User).filter(User.username == username).first() 
  
  except SQLAlchemyError as e:
      raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
  
  except Exception as e:
      raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def authenticate_user(db: Session, username: str, password: str):
  try:
    user = get_username(db, username)
    if not user or not verify_password(password, user.password_hash):
      raise HTTPException(status_code=401, detail='Invalid username or password.')
    
    return user
  
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
    
    return {'message': 'Signup successfuly!'}
  
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
    return {'message': f'{field} updated successfully'}

  except SQLAlchemyError as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')
