from datetime import timedelta
from app.models import Schedule
from app.services import convert_to_utc

def generate_schedules(intake):
  start = intake.start_datetime
  end = intake.end_datetime
  interval = intake.hour_interval

  schedules = []
  current = start

  while current.date() <= end.date():
    schedule = Schedule(
      user_id=intake.user_id,
      intake_id=intake.intake_id,
      scheduled_datetime=convert_to_utc(current),
      status_id=8 # ongoing
    )

    schedules.append(schedule)
    current += timedelta(hours=interval)

  return schedules