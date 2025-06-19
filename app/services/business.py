from datetime import timedelta
from zoneinfo import ZoneInfo
from app.models import Schedule
from app.constants import SCHEDULE_STATUS

def generate_schedules(intake):
  start = intake.start_datetime
  end = intake.end_datetime
  interval = intake.hour_interval
  manila_tz = ZoneInfo('Asia/Manila')
  
  if start.tzinfo is None:
    current = start.replace(tzinfo=manila_tz)
  else:
    current = start.astimezone(manila_tz)
  
  if end.tzinfo is None:
    end = end.replace(tzinfo=manila_tz)
  else:
    end = end.astimezone(manila_tz)
    
  print(f'Start: {current} | tzinfo: {current.tzinfo}')
  print(f'End: {end} | tzinfo: {end.tzinfo}')

  schedules = []

  while current <= end:
    print(f'Generated Schedule: {current}')
      
    schedule = Schedule(
      user_id=intake.user_id,
      intake_id=intake.intake_id,
      scheduled_datetime=current,
      status_id=SCHEDULE_STATUS['ONGOING']
    )
    schedules.append(schedule)
    current += timedelta(hours=interval)
    
  return schedules
