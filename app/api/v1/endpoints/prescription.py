from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from zoneinfo import ZoneInfo

from app.database.session import get_db
from app.core.security import verify_token
from app.crud import get_user, store_prescription
from app.services import inspect_day_duration
from app.schemas import Color_Base, Medicine_Base, Medicine_Compartment_Base, Intake_Base

router = APIRouter()

@router.post('/prescription', status_code=201)
async def add_prescription(
  color: Color_Base = Body(...),
  medicine: Medicine_Base = Body(...),
  medicine_compartment: Medicine_Compartment_Base = Body(...),
  intake: Intake_Base = Body(...),
  token_payload = Depends(verify_token),
  db: Session = Depends(get_db)):
  
  payload = token_payload['payload']
  user = get_user(db, payload['id'])

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
  start = intake.start_datetime
  end = intake.end_datetime
  now = datetime.now(ZoneInfo('UTC'))

  if start < now or end.date() < now.date():
    raise HTTPException(status_code=404, detail='Start or end datetime cannot be in the past.')
  
  if inspect_day_duration(start.date(), end.date(), 1):
    raise HTTPException(status_code=404, detail='Start datetime must be before end datetime.')

  if start.date() == now.date() and start.time() < now.time():
    raise HTTPException(status_code=404, detail='Start time must be in the future.')

  if not inspect_day_duration(start.date(), end.date(), 30):
    raise HTTPException(status_code=404, detail='The duration between start and end is too long. Maximum schedule duration is 30 days.')
  
  stored_prescription = store_prescription(
    db,
    color,
    medicine,
    medicine_compartment,
    intake,
    user.user_id)
  
  return stored_prescription
