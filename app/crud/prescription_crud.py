from fastapi import Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.models import Medicine, Medicine_Compartment, Intake, Prescription

def store_prescription(db: Session, medicine_data, medicine_compartment_data, intake_data, user_id):
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

    # Insert into prescription table
    prescription_table = Prescription(
      medicine_id=medicine_table.medicine_id,
      intake_id=intake_table.intake_id,
      user_id=user_id
    )
    db.add(prescription_table)

    # Insert into medicine_compartment table
    medicine_compartment_table = Medicine_Compartment(
      compartment_id=medicine_compartment_data.compartment_id,
      medicine_id=medicine_table.medicine_id,
      user_id=user_id
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
