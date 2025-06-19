from fastapi import APIRouter,  HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.core.security import verify_token
from app.services import convert_to_utc, inspect_day_duration, inspect_mins_duration

from app.crud.auth_crud import get_user
from app.crud.history_crud import get_specific_history, get_all_history, update_specific_history
from app.crud.schedule_crud import get_specific_schedule

from app.schemas import Intake_History_Read, Intake_History_Update
from app.constants import HISTORY_STATUS

router = APIRouter()

@router.get('/read/histories', response_model=List[Intake_History_Read], status_code=200)
def read_histories(token_payload = Depends(verify_token), db: Session = Depends(get_db)):
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
  
  schedule = get_specific_schedule(db, payload, None, data.schedule_id)

  if not schedule:
    raise HTTPException(status_code=404, detail='Schedule not found.')
  
  history = get_specific_history(db, payload, data.schedule_id, data.history_id)

  if not history:
    raise HTTPException(status_code=404, detail='History not found.')
  
  start = convert_to_utc(schedule.scheduled_datetime).replace(microsecond=0)
  end = convert_to_utc(data.history_datetime).replace(microsecond=0)

  if start == end:
    status = HISTORY_STATUS['COMPLETED']
  elif inspect_day_duration(start.date(), end.date(), 0) and inspect_mins_duration(start, end, 5):
    status = HISTORY_STATUS['COMPLETED']
  else:
    status = HISTORY_STATUS['LATE']

  updated_history = update_specific_history(db, payload, data.schedule_id, data.history_id, data.history_datetime, status)

  return updated_history
