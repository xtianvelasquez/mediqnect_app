from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime

from app.services import generate_schedules
from app.crud.schedule_crud import get_specific_schedule
from app.crud.general_crud import get_specific_color, get_specific_compartment
from app.models import Medicine, Medicine_Compartment, Intake, Color
from app.constants import MEDICINE_STATUS, INTAKE_STATUS, COMPARTMENT_STATUS

def get_specific_medicine(db: Session, user_id: int, medicine_id: int):
  try:
    return db.query(Medicine).filter(Medicine.user_id == user_id, Medicine.medicine_id == medicine_id).first()
  
  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')
  
def get_specific_intake(db: Session, user_id: int, intake_id: int):
  try:
    return db.query(Intake).filter(Intake.user_id == user_id, Intake.medicine_id == intake_id).first()
  
  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def get_all_intake(db: Session, user_id: int):
  sent_intakes = []

  try:
    intakes = (db.query(Intake).filter(Intake.user_id == user_id).order_by(Intake.start_datetime.asc()).all())
  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  if not intakes:
    return []
  
  for intake in intakes:
    intake_payload = {
      'user_id': intake.user_id,
      'intake_id': intake.intake_id,
      'start_datetime': intake.start_datetime,
      'end_datetime': intake.end_datetime,
      'medicine_id': intake.medicine.medicine_id,
      'medicine_name': intake.medicine.medicine_name,
      'net_content': intake.medicine.net_content,
      'expiration_date': intake.medicine.expiration_date,
      'color_name': intake.color.color_name,
      'status_name': intake.status.status_name
    }
    sent_intakes.append(intake_payload)

  return sent_intakes

def update_specific_medicine(
    db: Session,user_id: int,
    medicine_id: int,
    medicine_name: str,
    net_content: int,
    expiration_date: datetime,
    color_name: str
):
  try:
    medicine = get_specific_medicine(db, user_id, medicine_id)

    if medicine_name not in [None, '']:
      medicine.medicine_name = medicine_name
    if net_content not in [None, '', 0]:
      medicine.net_content = net_content
    if expiration_date not in [None, '']:
      medicine.expiration_date = expiration_date

    if color_name is not None and medicine.intake is not None:
      intake = get_specific_intake(db, user_id, medicine.intake.intake_id)
      if intake:
        existing_color = get_specific_color(db, color_name)
        if existing_color:
          intake.color_id = existing_color.color_id
        else:
          new_color = Color(color_name=color_name)
          db.add(new_color)
          db.commit()
          db.refresh(new_color)
          intake.color_id=new_color.color_id

    db.commit()
    db.refresh(medicine)
    
    return {'message': 'Your medicine has been successfully updated.', 'updated_medicine': medicine}

  except SQLAlchemyError as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def delete_specific_medicine(db: Session, user_id: int, medicine_id: int):
  try:
    prescription = get_specific_medicine(db, user_id, medicine_id)

    compartment = get_specific_compartment(db, prescription.medicine_compartment.compartment_id)
    if not compartment:
      raise HTTPException(status_code=404, detail='Compartment not found.')
  
    compartment.status_id = COMPARTMENT_STATUS['VACANT']
    db.delete(prescription)
    db.commit()
  
    return {'message': 'Prescription deleted and compartment marked as vacant.'}
  
  except SQLAlchemyError as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def store_prescription(
    db: Session,
    color_data,
    medicine_data,
    medicine_compartment_data,
    intake_data,
    user_id: int):

  try:
    # Use a transaction block for atomicity
    with db.begin_nested():  
      # Check if color already exists
      existing_color = get_specific_color(db, color_data.color_name)
      if existing_color:
        color_table = existing_color
      else:
        color_table = Color(color_name=color_data.color_name)
        db.add(color_table)
        db.flush()

      # Insert medicine data
      medicine_dict = medicine_data.dict()
      medicine_dict.update({
        'user_id': user_id,
        'status_id': MEDICINE_STATUS['AVAILABLE'] # available
      })

      medicine_table = Medicine(**medicine_dict)
      db.add(medicine_table)
      db.flush()

      # Insert intake data
      intake_dict = intake_data.dict()
      intake_dict.update({
        'user_id': user_id,
        'medicine_id': medicine_table.medicine_id,
        'color_id': color_table.color_id,
        'status_id': INTAKE_STATUS['PENDING'] # pending
      })
      intake_table = Intake(**intake_dict)
      db.add(intake_table)
      db.flush()

      # Insert medicine compartment data
      medicine_compartment_table = Medicine_Compartment(
        user_id=user_id,
        compartment_id=medicine_compartment_data.compartment_id,
        medicine_id=medicine_table.medicine_id
      )
      db.add(medicine_compartment_table)

      # Check if schedules for intake are already generated
      schedules_exist = get_specific_schedule(db, user_id, intake_table.intake_id, None)
      if not schedules_exist:
        schedules = generate_schedules(intake_table)
        intake_table.is_scheduled = True
        db.add_all(schedules)

      # Check if compartment is already occupied
      compartment_table = get_specific_compartment(db, medicine_compartment_table.compartment_id)
      if compartment_table.status_id != COMPARTMENT_STATUS['OCCUPIED']:
        compartment_table.status_id = COMPARTMENT_STATUS['OCCUPIED'] # occupied

    # Commit changes
    try:
      db.commit()
    except IntegrityError as e:
      db.rollback()
      raise HTTPException(status_code=400, detail=f'Data integrity issue: {str(e)}')
    
    return {'message': 'Your prescription details have been successfully added.'}
  
  except SQLAlchemyError as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')
