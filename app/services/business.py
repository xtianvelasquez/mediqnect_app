from datetime import timedelta
from app.schemas import Schedule_Create

def generate_schedules(intake):
  start = intake.start_datetime
  end = intake.end_date
  interval = intake.hour_interval

  schedules = []
  first = start

  while first.date() <= end:
    schedule = Schedule_Create(
      user_id=intake.user_id,
      intake_id=intake.intake_id,
      scheduled_datetime=first,
      status_id=8 # ongoing
    )

    schedules.append(schedule)
    first += timedelta(hours=interval)

  return schedules