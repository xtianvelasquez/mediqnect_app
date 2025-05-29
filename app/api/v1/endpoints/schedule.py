from fastapi import APIRouter,  HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.core import verify_token
from app.crud import get_user, get_all_schedule, delete_specific_schedule
from app.schemas import Schedule_Read, Schedule_Delete

router = APIRouter()

@router.get('/schedules', response_model=List[Schedule_Read], status_code=200)
def get_schedules(token_payload = Depends(verify_token), db: Session = Depends(get_db)):
  payload = token_payload.get('payload', {}).get('id')
  user = get_user(db, payload)

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
  schedules = get_all_schedule(db, payload)

  return schedules

@router.post('/delete/schedule', status_code=200)
def delete_schedule(data: Schedule_Delete, token_payload = Depends(verify_token), db: Session = Depends(get_db)):
  payload = token_payload.get('payload', {}).get('id')
  user = get_user(db, payload)

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
  schedule = delete_specific_schedule(db, payload, data.intake_id, data.schedule_id)

  return schedule
