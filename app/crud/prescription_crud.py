from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException

from app.services import generate_schedules
from app.models import Medicine, Medicine_Compartment, Compartment, Intake, Schedule, Color
from app.constants import MEDICINE_STATUS, INTAKE_STATUS, COMPARTMENT_STATUS

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
      schedules_exist = db.query(Schedule).filter(
        Schedule.user_id == user_id,
        Schedule.intake_id == intake_table.intake_id
      ).first()
      if not schedules_exist:
        schedules = generate_schedules(intake_table)
        intake_table.is_scheduled = True
        db.add_all(schedules)

      # Check if compartment is already occupied
      compartment_table = db.query(Compartment).filter(Compartment.compartment_id == medicine_compartment_table.compartment_id).first()
      if compartment_table:
        compartment_table.status_id = COMPARTMENT_STATUS['OCCUPIED'] # occupied

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

#  def edit_prescription(db: Session, user_id, intake_id: int, data: dict):
#    schedule = db.query(Schedule).filter(Schedule.id == edit_data.schedule_id).first()
#    if not schedule:
#        raise HTTPException(status_code=404, detail="Schedule not found")
#
#    # Update Schedule fields
#    if edit_data.scheduled_datetime is not None:
#        schedule.scheduled_datetime = edit_data.scheduled_datetime
#
#    # Fetch and update related Medicine
#    medicine = db.query(Medicine).filter(Medicine.id == schedule.medicine_id).first()
#    if not medicine:
#        raise HTTPException(status_code=404, detail="Medicine not found")
#
#    if edit_data.medicine_name is not None:
#        medicine.name = edit_data.medicine_name
#
#    if edit_data.expiration_date is not None:
#        medicine.expiration_date = edit_data.expiration_date
#
#    # Commit once
#    db.commit()
#    db.refresh(schedule)
#    db.refresh(medicine)
#
#    return {
#        "message": "Schedule and medicine updated successfully.",
#        "schedule_id": schedule.id,
#        "medicine_id": medicine.id
#    }
