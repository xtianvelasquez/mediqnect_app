from fastapi.encoders import jsonable_encoder
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from datetime import datetime
from zoneinfo import ZoneInfo
import json

from app.mq_publisher import publish_expired
from app.crud.general_crud import get_specific_compartment
from app.models import Medicine, Medicine_Compartment
from app.constants import MEDICINE_STATUS, COMPARTMENT_STATUS

from app.database.session import SessionLocal
from app.models import Medicine, Compartment

def get_all_medicine(db: Session, user_id: int):
  try:
    medicines = db.query(Medicine).filter(Medicine.user_id == user_id, Medicine.status_id == MEDICINE_STATUS['AVAILABLE']).all()
    return medicines
  
  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
  
  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def store_medicine(
    db: Session,
    user_id: int,
    medicine_data,
    medicine_compartment_data
):
  try:
    with db.begin_nested():
      medicine_dict = medicine_data.dict()
      medicine_dict.update({
        'user_id': user_id,
        'status_id': MEDICINE_STATUS['AVAILABLE']
      })

      medicine_table = Medicine(**medicine_dict)
      db.add(medicine_table)
      db.flush()

      medicine_compartment_table = Medicine_Compartment(
        user_id=user_id,
        compartment_id=medicine_compartment_data.compartment_id,
        medicine_id=medicine_table.medicine_id
      )
      db.add(medicine_compartment_table)

      compartment_table = get_specific_compartment(db, medicine_compartment_data.compartment_id)
      if compartment_table.status_id != COMPARTMENT_STATUS['OCCUPIED']:
        compartment_table.status_id = COMPARTMENT_STATUS['OCCUPIED']

    try:
      db.commit()
    except IntegrityError as e:
      db.rollback()
      raise HTTPException(status_code=400, detail=f'Data integrity issue: {str(e)}')
    
    return {'message': 'Your medicine details have been successfully added.'}
  
  except SQLAlchemyError as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def mark_expired_medicines():
  with SessionLocal() as db:
    now = datetime.now(ZoneInfo('Asia/Manila')).replace(second=0, microsecond=0)
    today = now.date()

    medicines = db.query(Medicine).filter(
      Medicine.status_id != MEDICINE_STATUS['EXPIRED'],
      Medicine.expiration_date <= today
    ).all()

    for medicine in medicines:
      compartment = db.query(Compartment).filter(
        Compartment.compartment_id == medicine.medicine_compartment.compartment_id
      ).first()
      if compartment:
        publish_expired(json.dumps(jsonable_encoder(compartment)), f'mediqnect/alarm/{compartment.compartment_id}')
        compartment.status_id = COMPARTMENT_STATUS['VACANT']
        
      medicine.status_id = MEDICINE_STATUS['EXPIRED']
      db.delete(medicine)

    db.commit()
    print(f"[{now}] Marked {len(medicines)} medicine(s) as EXPIRED.")

scheduler = BackgroundScheduler()
scheduler.add_job(mark_expired_medicines, 'interval', minutes=1)
scheduler.start()
