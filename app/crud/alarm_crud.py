from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.models import Medicine_Compartment, Schedule, Intake_History
from app.constants import SCHEDULE_STATUS, HISTORY_STATUS

def check_and_send_alarms(db: Session, user_id: int):
  now = datetime.now(ZoneInfo('Asia/Manila')).replace(second=0, microsecond=0)

  print(f'Checking alarms for user {user_id} at {now}')

  sent_alarms = []

  schedules = db.query(Schedule).filter(
    Schedule.user_id == user_id,
    Schedule.status_id == SCHEDULE_STATUS['ONGOING']
  ).all()

  print(f'Found {len(schedules)} schedules to check.')

  for schedule in schedules:
    print(f'schedule {schedule.scheduled_datetime}')
    schedule_aware = schedule.scheduled_datetime.replace(tzinfo=ZoneInfo('Asia/Manila'))
    # Correct timezone interpretation
    print(f'schedule_aware {schedule_aware}')

    # Accurate comparison with current time
    if schedule_aware == now:
      intake = schedule.intake

      if not intake:
        print(f'Skipping schedule {schedule.schedule_id} - intake missing.')
        continue

      med_compartment = db.query(Medicine_Compartment).filter(
        Medicine_Compartment.medicine_id == intake.medicine_id
      ).first()

      if not med_compartment:
        print(f'Skipping schedule {schedule.schedule_id} - no compartment for medicine ID {intake.medicine_id}.')
        continue

      mqtt_payload = {
        'user_id': schedule.user_id,
        'intake_id': schedule.intake_id,
        'schedule_id': schedule.schedule_id,
        'scheduled_datetime': schedule.scheduled_datetime,
        'dose': schedule.intake.dose,
        'medicine_name': med_compartment.medicine.medicine_name,
        'compartment_id': med_compartment.compartment.compartment_id,
      }
      sent_alarms.append(mqtt_payload)

  return sent_alarms

def mark_missed_schedules():
  with SessionLocal() as db:
    now = datetime.now(ZoneInfo('Asia/Manila')).replace(second=0, microsecond=0)
    now_naive = now.replace(tzinfo=None)
    overdue_time = now_naive - timedelta(minutes=6)

    schedules = db.query(Schedule).filter(
      Schedule.status_id == SCHEDULE_STATUS['ONGOING'],
      Schedule.scheduled_datetime < overdue_time
    ).all()

    for schedule in schedules:
      missed_intake = Intake_History(
        user_id=schedule.user_id,
        schedule_id=schedule.schedule_id,
        status_id=HISTORY_STATUS['MISSED']
      )
      schedule.status_id = SCHEDULE_STATUS['ENDED']
      db.add(schedule)
      db.add(missed_intake)

    db.commit()
    print(f'[{now}] Marked {len(schedules)} schedule(s) as MISSED.')

scheduler = BackgroundScheduler()
scheduler.add_job(mark_missed_schedules, 'interval', minutes=1)
scheduler.start()
