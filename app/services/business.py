from datetime import timedelta
from app.models import Schedule
from app.services import convert_to_utc
from app.constants import SCHEDULE_STATUS
from app.config import LOCAL_TIMEZONE
from zoneinfo import ZoneInfo

LOCAL_TIMEZONE = ZoneInfo('Asia/Manila')


def generate_schedules(intake):
  start = intake.start_datetime.replace(tzinfo=LOCAL_TIMEZONE)
  end = intake.end_datetime.replace(tzinfo=LOCAL_TIMEZONE)
  interval = intake.hour_interval

  schedules = []
  current = start

  while current <= end:
    schedule = Schedule(
      user_id=intake.user_id,
      intake_id=intake.intake_id,
      scheduled_datetime=current,
      status_id=SCHEDULE_STATUS['ONGOING'] # ongoing
    )

    schedules.append(schedule)
    current += timedelta(hours=interval)

  return schedules
