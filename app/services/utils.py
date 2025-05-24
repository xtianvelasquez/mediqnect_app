from datetime import date, datetime, timedelta
from app.models import Schedule

def inspect_duration(start, end, interval):
  result = (end - start) < timedelta(days=interval)
  return result

def generate_schedules(intake):
  start = intake.start_datetime
  end = intake.end_date
  interval = intake.hour_interval

  schedules = []
  first = start

  while first.date() <= end:
    schedule = Schedule(
      user_id=intake.user_id,
      intake_id=intake.intake_id,
      scheduled_datetime=first,
      status_id=8 # ongoing
    )

    schedules.append(schedule)
    first += timedelta(hours=interval)

  return schedules
