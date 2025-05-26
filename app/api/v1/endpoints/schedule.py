from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from zoneinfo import ZoneInfo

from app.database.session import get_db
from app.core import verify_token
from app.crud import get_user
from app.schemas import Schedule_Read

router = APIRouter()

@router.get('/schedules', response_model=Schedule_Read, status_code=200)
def get_schedules(token_payload = Depends(verify_token), db: Session = Depends(get_db)):
  payload = token_payload['payload']
  user = get_user(db, payload['id'])

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
