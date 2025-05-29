from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.services import convert_datetime
from app.constants import SCHEDULE_STATUS
from app.models import Medicine_Compartment, Schedule, Color

def get_specific_schedule(db: Session, user_id: int, intake_id: int, schedule_id: int):
  try:
    return db.query(Schedule).filter(
    Schedule.user_id == user_id,
    Schedule.intake_id == intake_id,
    Schedule.schedule_id == schedule_id).first()
  
  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def get_all_schedule(db: Session, user_id: int):
  sent_schedules = []

  try:
    schedules = (db.query(Schedule).filter(Schedule.user_id == user_id, Schedule.status_id == SCHEDULE_STATUS['ONGOING']).order_by(Schedule.scheduled_datetime.asc()).all())

  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

  for schedule in schedules:
    medicine_compartment = db.query(Medicine_Compartment).filter(Medicine_Compartment.medicine_id == schedule.intake.medicine_id).first()
    color = db.query(Color).filter(Color.color_id == schedule.intake.color_id).first()

    if medicine_compartment:
      schedule_payload = {
        'user_id': schedule.user_id,
        'intake_id': schedule.intake_id,
        'scheduled_datetime': convert_datetime(schedule.scheduled_datetime),
        'schedule_id': schedule.schedule_id,
        'medicine_name': medicine_compartment.medicine.medicine_name,
        'color_name': color.color_name
      }

      sent_schedules.append(schedule_payload)

  return sent_schedules

def delete_specific_schedule(db: Session, user_id: int, intake_id: int, schedule_id: int):
  schedule = get_specific_schedule(db, user_id, intake_id, schedule_id)

  if not schedule:
    raise HTTPException(status_code=404, detail=f'Schedule not found.')

  db.delete(schedule)
  db.commit()

  return {'message': 'The schedule has been successfully deleted.'}
