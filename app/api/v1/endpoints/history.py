from fastapi import APIRouter,  HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.core.security import verify_token
from app.crud import get_user, get_all_history, get_specific_history, get_specific_schedule, update_history
from app.services import convert_to_utc, inspect_mins_duration
from app.constants import HISTORY_STATUS
from app.schemas import Intake_History_Read, Intake_History_Update

router = APIRouter()

@router.get('/histories', response_model=List[Intake_History_Read], status_code=200)
def get_histories(token_payload = Depends(verify_token), db: Session = Depends(get_db)):
  payload = token_payload.get('payload', {}).get('id')
  user = get_user(db, payload)

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
  history = get_all_history(db, payload)

  return history

@router.post('/update/history', status_code=200)
def update_history(
  data: Intake_History_Update,
  token_payload = Depends(verify_token),
  db: Session = Depends(get_db)):
  
  payload = token_payload.get('payload', {}).get('id')
  user = get_user(db, payload)

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
  history = get_specific_history(db, payload, data.schedule_id, data.history_id)

  if not history:
    raise HTTPException(status_code=404, detail=f'History not found.')
  
  schedule = get_specific_schedule(db, payload, None, data.schedule_id)

  if not schedule:
    raise HTTPException(status_code=404, detail=f'Schedule not found.')
  
  if inspect_mins_duration(schedule.scheduled_datetime, convert_to_utc(data.history_datetime), 3):
    status = HISTORY_STATUS['COMPLETED']
  else:
    status = HISTORY_STATUS['LATE']

  updated_history = update_history(db, payload, data.schedule_id, data.history_id, data.history_datetime, status)

  return updated_history
