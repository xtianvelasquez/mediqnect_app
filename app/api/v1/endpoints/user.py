from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core import create_token, verify_token, validate_password
from app.models import User
from app.schemas import User_Read

router = APIRouter()

@router.get('/user', response_model=User_Read, status_code=200)
async def current_user(token_payload = Depends(verify_token), db: Session = Depends(get_db)):

  user = db.query(User).filter(User.user_id == token_payload['id']).first()

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
  return {
    'user_id': user.user_id,
    'username': user.username,
    'date_created': user.date_created,
    'date_modified': user.date_modified
  }

@router.get('/protected', status_code=200)
async def protected_route(user: dict = Depends(verify_token)):
  return {"message": f"Welcome, {user['sub']}"}
