from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.services import convert_datetime
from app.models import Intake, Intake_History

def get_specific_history(db: Session, user_id: int, schedule_id: int, history_id: int):
  try:
    query = db.query(Intake_History).filter(Intake_History.user_id == user_id, Intake_History.schedule_id == schedule_id)
    
    if history_id is not None:
      query = query.filter(Intake_History.history_id == history_id)

    return query.first()

  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def get_all_history(db: Session, user_id: int):
  sent_histories = []

  try:
    histories = (db.query(Intake_History).filter(Intake_History.user_id == user_id).order_by(Intake_History.history_datetime.asc()).all())
  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e.orig)}')
  
  if not histories:
    return []
  
  for history in histories:
    intake = db.query(Intake).filter(Intake.intake_id == history.schedule.intake_id).first()

    if intake:
      history_payload = {
        'user_id': history.user_id,
        'schedule_id': history.schedule_id,
        'scheduled_datetime': convert_datetime(history.schedule.scheduled_datetime),
        'history_id': history.history_id,
        'history_datetime': convert_datetime(history.history_datetime),
        'medicine_name': intake.medicine.medicine_name,
        'status_name': history.status.status_name,
      }
      sent_histories.append(history_payload)

  return sent_histories

def update_specific_history(db: Session, user_id: int, schedule_id: int, history_id: int, history_datetime: datetime, status: int):
  try:
    history = get_specific_history(db, user_id, schedule_id, history_id)

    history.history_datetime = history_datetime
    history.status_id = status

    db.commit()
    db.refresh(history)

    return {'message': 'Your missed medicine has been successfully updated.'}
  
  except SQLAlchemyError as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')
