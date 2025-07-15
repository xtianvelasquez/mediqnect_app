from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.database.session import SessionLocal
from app.models import Schedule, Intake_History

COMPARTMENT_STATUS = {
  'VACANT': 1,
  'OCCUPIED': 2
}

MEDICINE_STATUS = {
  'AVAILABLE': 3,
  'UNAVAILABLE': 4,
  'EXPIRED': 5
}

INTAKE_STATUS = {
  'PENDING': 6,
  'FULFILLED': 7
}

SCHEDULE_STATUS = {
  'ONGOING': 8,
  'ENDED': 9
}

HISTORY_STATUS = {
  'COMPLETED': 10,
  'LATE': 11,
  'MISSED': 12
}

def mark_missed_schedules():
  with SessionLocal() as db:
    now = datetime.now(ZoneInfo('Asia/Manila')).replace(second=0, microsecond=0)
    now_naive = now.replace(tzinfo=None)
    overdue_time = now_naive - timedelta(minutes=5)

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
