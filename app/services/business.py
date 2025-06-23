from datetime import timedelta
from app.services import convert_to_tz
from app.models import Schedule
from app.constants import SCHEDULE_STATUS

def generate_schedules(intake):
  current = convert_to_tz(intake.start_datetime)
  end = convert_to_tz(intake.end_datetime)
  interval = intake.hour_interval
    
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
