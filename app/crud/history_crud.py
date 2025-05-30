from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.services import convert_datetime
from app.models import Intake, Intake_History

def get_all_history(db: Session, user_id):
    sent_histories = []

    try:
        histories = (
            db.query(Intake_History)
            .filter(Intake_History.user_id == user_id)
            .order_by(Intake_History.history_datetime.asc())
            .all()
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e.orig)}")

    if not histories:
        return []  # Avoid unnecessary iterations

    for history in histories:
        intake = db.query(Intake).filter(Intake.intake_id == history.schedule.intake_id).first()
        
        if not intake:
            continue  # Skip if intake record is missing

        history_payload = {
            "user_id": history.user_id,
            "schedule_id": history.schedule_id,
            "scheduled_datetime": history.schedule.scheduled_datetime,
            "history_id": history.history_id,
            "history_datetime": history.history_datetime,
            "medicine_name": intake.medicine.medicine_name,
            "status_name": history.status.status_name,
        }

        sent_histories.append(history_payload)

    return sent_histories
