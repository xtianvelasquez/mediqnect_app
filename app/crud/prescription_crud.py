from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException

from app.services import generate_schedules
from app.models import Medicine, Medicine_Compartment, Intake, Color

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
      existing_color = db.query(Color).filter(Color.color_name == color_data.color_name).first()
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
        'status_id': 3 # available
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
        'status_id': 6 # pending
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

      schedules = generate_schedules(intake_table)
      db.add_all(schedules)

    # Commit changes
    try:
      db.commit()
    except IntegrityError as e:
      db.rollback()
      raise HTTPException(status_code=400, detail=f'Data integrity issue: {str(e)}')
    
  except SQLAlchemyError as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

  return {'message': 'Your prescription details have been successfully added.'}