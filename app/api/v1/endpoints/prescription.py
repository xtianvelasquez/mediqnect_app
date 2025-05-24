from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core import verify_token
from app.crud import get_user, store_prescription, get_specific_status
from app.services import inspect_duration
from app.schemas import Medicine_Create, Medicine_Compartment_Base, Intake_Create, Color_Base

router = APIRouter()

@router.post('/prescriptions', status_code=201)
async def add_prescription(
  color: Color_Base = Body(...),
  medicine: Medicine_Create = Body(...),
  medicine_compartment: Medicine_Compartment_Base = Body(...),
  intake: Intake_Create = Body(...),
  token_payload = Depends(verify_token),
  db: Session = Depends(get_db)):
  
  payload = token_payload['payload']
  user = get_user(db, payload['id'])

  # Status
  medicine_default_status = get_specific_status(db, 'available')
  prescription_default_status = get_specific_status(db, 'ongoing')
  compartment_change_status = get_specific_status(db, 'occupied')

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
  stored_prescription = store_prescription(
    db,
    color,
    medicine,
    medicine_compartment,
    intake,
    user.user_id,
    medicine_default_status.status_id,
    prescription_default_status.status_id)
  
  return stored_prescription
