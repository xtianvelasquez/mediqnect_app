from fastapi import APIRouter,  HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
import traceback

from app.database.session import get_db
from app.core.security import verify_token
from app.services import inspect_day_duration, inspect_mins_duration, convert_to_tz

from app.crud.auth_crud import get_user
from app.crud.prescription_crud import get_specific_intake
from app.crud.history_crud import get_specific_history, get_all_history, update_specific_history
from app.crud.schedule_crud import get_specific_schedule
from app.services.utils import count_datetime_gap
from app.models import Schedule
from app.schemas import Intake_History_Read, Intake_History_Update
from app.constants import HISTORY_STATUS, SCHEDULE_STATUS

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
  
  intake = get_specific_intake(db, payload, schedule.intake_id)
  if not intake:
    raise HTTPException(status_code=404, detail='Intake not found.')
  
  if intake.medicine.net_content <= 0:
    raise HTTPException(status_code=400, detail='Medicine is already empty. Cannot confirm intake.')

  if intake.medicine.net_content < intake.dose:
    raise HTTPException(status_code=400, detail='Not enough medicine left to confirm this dose.')
  
  start = convert_to_tz(schedule.scheduled_datetime)
  end = convert_to_tz(data.history_datetime)

  if start == end:
    status = HISTORY_STATUS['COMPLETED']
  elif inspect_day_duration(start.date(), end.date(), 0) and inspect_mins_duration(start, end, 5):
    status = HISTORY_STATUS['COMPLETED']
  else:
    status = HISTORY_STATUS['LATE']

    gap = count_datetime_gap(start, end)
    print(f'Gap between {start} and {end} is {gap} minutes')

    ongoing_schedules = db.query(Schedule).filter(
    Schedule.user_id == payload,
    Schedule.intake_id == schedule.intake.intake_id,
    Schedule.status_id == SCHEDULE_STATUS['ONGOING']).all()
  
    for ongoing_schedule in ongoing_schedules:
      old_dt = ongoing_schedule.scheduled_datetime
      new_dt = old_dt + timedelta(minutes=gap)
      ongoing_schedule.scheduled_datetime = new_dt
      db.add(ongoing_schedule)
  
    try:
      db.commit()
    except Exception as e:
      db.rollback()
      print(traceback.format_exc())  # log full traceback
      raise HTTPException(status_code=500, detail=f'Failed to update schedules: {str(e)}')

  intake.medicine.net_content -= intake.dose
  db.add(intake)

  try:
    db.commit()
    db.refresh(intake)
  except Exception as e:
    db.rollback()
    print(traceback.format_exc()) # log full traceback
    raise HTTPException(status_code=500, detail=f'Failed to update medicine: {str(e)}')
  
  updated_history = update_specific_history(db, payload, data.schedule_id, data.history_id, data.history_datetime, status)

  return updated_history
