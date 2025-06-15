from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from zoneinfo import ZoneInfo

from app.database.session import get_db
from app.core.security import verify_token
from app.services import inspect_day_duration
from app.crud.auth_crud import get_user
from app.crud.prescription_crud import get_all_intake, get_specific_medicine, update_specific_medicine, store_prescription, delete_specific_medicine
from app.schemas import Color_Base, Medicine_Base, Medicine_Edit, Medicine_Delete, Medicine_Compartment_Base, Intake_Base, Intake_Read

router = APIRouter()

@router.get('/read/prescription', response_model=List[Intake_Read], status_code=200)
async def read_prescription(token_payload = Depends(verify_token), db: Session = Depends(get_db)):
  payload = token_payload.get('payload', {}).get('id')
  user = get_user(db, payload)

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
  intakes = get_all_intake(db, payload)

  return intakes

@router.post('/create/prescription', status_code=201)
async def create_prescription(
  color: Color_Base = Body(...),
  medicine: Medicine_Base = Body(...),
  medicine_compartment: Medicine_Compartment_Base = Body(...),
  intake: Intake_Base = Body(...),
  token_payload = Depends(verify_token),
  db: Session = Depends(get_db)):
  
  payload = token_payload.get('payload', {}).get('id')
  user = get_user(db, payload)

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

@router.post('/delete/prescription', status_code=200)
def delete_prescription(data: Medicine_Delete, token_payload = Depends(verify_token), db: Session = Depends(get_db)):
  payload = token_payload.get('payload', {}).get('id')
  user = get_user(db, payload)

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')

  prescription = get_specific_medicine(db, payload, data.medicine_id)
  if not prescription:
    raise HTTPException(status_code=404, detail='Schedule not found.')
  
  if not prescription.medicine_compartment:
    raise HTTPException(status_code=404, detail='Medicine compartment not assigned.')
  
  medicine = delete_specific_medicine(db, payload, data.medicine_id)

  return medicine

@router.post('/update/medicine', status_code=200)
def update_medicine(data: Medicine_Edit, token_payload = Depends(verify_token), db: Session = Depends(get_db)):
  payload = token_payload.get('payload', {}).get('id')
  user = get_user(db, payload)

  print('data:', data)
  print('payload:', payload)
  print('token_payload:', token_payload)

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
  medicine = get_specific_medicine(db, payload,data.medicine_id)

  if not medicine:
    raise HTTPException(status_code=404, detail='Medicine not found.')
    
  if inspect_day_duration(datetime.utcnow(), medicine.modified_at, 1):
    raise HTTPException(status_code=403, detail='Medicine can only be modified after a day.')
  
  medicine = update_specific_medicine(
    db,
    payload,
    data.medicine_id,
    data.medicine_name,
    data.net_content,
    data.expiration_date,
    data.color_name)

  return medicine
