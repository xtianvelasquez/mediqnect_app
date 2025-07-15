from fastapi import APIRouter,  HTTPException, Body, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.core.security import verify_token
from app.crud.auth_crud import get_user
from app.crud.medicine_crud import get_all_medicine, store_medicine

from app.schemas import Medicine_Base, Medicine_Read, Medicine_Compartment_Base, Clean_Compartment

router = APIRouter()

@router.post('/create/medicine', status_code=201)
def create_medicine(
  medicine: Medicine_Base = Body(...),
  medicine_compartment: Medicine_Compartment_Base = Body(...),
  token_payload=Depends(verify_token),
  db: Session = Depends(get_db)):

  user_id = token_payload.get('payload', {}).get('id')
  user = get_user(db, user_id)

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
  return store_medicine(db, user_id, medicine, medicine_compartment)

@router.get('/read/medicines', response_model=List[Medicine_Read], status_code=200)
def read_medicines(token_payload=Depends(verify_token), db: Session=Depends(get_db)):
  user_id = token_payload.get('payload', {}).get('id')
  user = get_user(db, user_id)

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
  medicines = get_all_medicine(db, user_id)
  
  sent_medicines = []
  for medicine in medicines:
    sent_medicines.append({
      'medicine_name': medicine.medicine_name,
      'form_id': medicine.form_id,
      'net_content': medicine.net_content,
      'expiration_date': medicine.expiration_date,
      'medicine_id': medicine.medicine_id,
      'user_id': medicine.user_id,
      'created_at': medicine.created_at,
      'modified_at': medicine.modified_at,
      'status_name': medicine.status.status_name,
    })

  return sent_medicines

@router.post('/clean/compartment', status_code=200)
def clean_medicine(data: Clean_Compartment, token_payload=Depends(verify_token), db: Session=Depends(get_db)):
  user_id = token_payload.get('payload', {}).get('id')
  user = get_user(db, user_id)

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')

  print(data)

  return {'message': 'Please wait for 5 minutes.'}
