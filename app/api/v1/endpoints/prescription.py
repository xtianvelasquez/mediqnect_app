from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core import verify_token
from app.crud import get_user, store_prescription
from app.schemas import Medicine_Create, Medicine_Compartment_Create, Intake_Create, Color_Base

router = APIRouter()

@router.post('/prescriptions', status_code=201)
async def add_prescription(
  color: Color_Base = Body(...),
  medicine: Medicine_Create = Body(...),
  medicine_compartment: Medicine_Compartment_Create = Body(...),
  intake: Intake_Create = Body(...),
  token_payload = Depends(verify_token),
  db: Session = Depends(get_db)):
  
  payload = token_payload['payload']
  user = get_user(db, payload['id'])

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
  stored_prescription = store_prescription(
    db,
    color,
    medicine,
    medicine_compartment,
    intake,
    user.user_id)
  
  return stored_prescription
