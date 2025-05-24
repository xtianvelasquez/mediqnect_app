from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.models import Medicine, Medicine_Compartment, Intake, Color

def store_prescription(
    db: Session,
    color_data,
    medicine_data,
    medicine_compartment_data,
    intake_data,
    user_id: int):
  
  try:
    # Insert into medicine table
    medicine_table = Medicine(**medicine_data.dict())
    db.add(medicine_table)
    db.flush()
    db.refresh(medicine_table)

    # Insert into intake table
    intake_table = Intake(**intake_data.dict())
    db.add(intake_table)
    db.flush()
    db.refresh(intake_table)

    # Insert into color table
    color_table = Color(
      color_name=color_data.color_name
    )
    db.add(color_table)
    db.flush()
    db.refresh(color_table)

    # Insert into medicine_compartment table
    medicine_compartment_table = Medicine_Compartment(
      user_id=user_id,
      compartment_id=medicine_compartment_data.compartment_id,
      medicine_id=medicine_table.medicine_id
    )
    db.add(medicine_compartment_table)

    db.commit()

    return {'message': 'Prescription details added successfully!'}

  except SQLAlchemyError as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')