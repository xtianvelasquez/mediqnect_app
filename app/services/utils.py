from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from app.config import timezone

def convert_datetime(d: datetime) -> str:
  utc_dt = d.replace(tzinfo=ZoneInfo('UTC'))
  ph_dt = utc_dt.astimezone(ZoneInfo(timezone))
  formatted_dt = ph_dt.strftime('%Y-%m-%d %H:%M')

  return formatted_dt

def convert_to_utc(dt: datetime) -> datetime:
  if dt.tzinfo is None or dt.utcoffset() is None:
    raise ValueError(f'Datetime must be timezone-aware. Got: {dt}')

  return dt.astimezone(ZoneInfo('UTC'))

def inspect_day_duration(start: datetime, end: datetime, interval: int) -> bool:
  return abs(end - start) <= timedelta(days=interval)

def inspect_mins_duration(start: datetime, end: datetime, interval: int) -> bool:
  return abs(end - start) <= timedelta(minutes=interval)
