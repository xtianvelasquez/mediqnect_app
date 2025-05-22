from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core import verify_token
from app.crud import get_user, store_prescription
from app.services import inspect_duration
from app.schemas import Medicine_Create, Medicine_Compartment_Create, Intake_Create, Prescription_Create

router = APIRouter()

@router.post('/prescription')
async def add_prescription(
  medicine: Medicine_Create | None = Body(None),
  medicine_compartment: Medicine_Compartment_Create | None = Body(None),
  intake: Intake_Create | None = Body(None),
  prescription: Prescription_Create | None = Body(None),
  token_payload = Depends(verify_token),
  db: Session = Depends(get_db)):
  
  payload = token_payload['payload']
  user = get_user(db, payload['id'])

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
  if inspect_duration(intake.start_datetime.date(), intake.end_date, 0):
    raise HTTPException(status_code=403, detail='Start date is ahead than end date. Please try again.')
  
  stored_prescription = store_prescription(db, medicine, medicine_compartment, intake, prescription, user.user_id)
  
  return stored_prescription
