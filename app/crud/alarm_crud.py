from sqlalchemy.orm import Session
from datetime import datetime
from zoneinfo import ZoneInfo

from app.services import convert_datetime
from app.models import Medicine_Compartment, Schedule

def check_and_send_alarms(db: Session, user_id: int):
  now = datetime.now(ZoneInfo('UTC')).replace(second=0, microsecond=0)
  print(f'Checking alarms for user {user_id} at {convert_datetime(now)}') # Testing

  sent_alarms = []

  schedules = db.query(Schedule).filter(Schedule.user_id == user_id, Schedule.scheduled_datetime == now).all()
  for schedule in schedules:
    medicine_compartment = db.query(Medicine_Compartment).filter(Medicine_Compartment.medicine_id == schedule.intake.medicine_id).first()

    if medicine_compartment:
      mqtt_payload = {
        'user_id': schedule.user_id,
        'intake_id': schedule.intake_id,
        'schedule_id': schedule.schedule_id,
        'scheduled_datetime': convert_datetime(schedule.scheduled_datetime),
        'medicine_name': medicine_compartment.medicine.medicine_name,
        'compartment_id': medicine_compartment.compartment.compartment_id
      }

      sent_alarms.append(mqtt_payload)

  return sent_alarms
