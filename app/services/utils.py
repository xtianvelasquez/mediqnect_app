from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from app.config import LOCAL_TIMEZONE

def convert_datetime(dt: datetime) -> str:
  if dt is None:
    return None

  if dt.tzinfo is None or dt.utcoffset() is None:
    dt = dt.replace(tzinfo=ZoneInfo('UTC'))

  local_dt = dt.astimezone(ZoneInfo(LOCAL_TIMEZONE))

  return local_dt.strftime('%Y-%m-%d %H:%M')

def convert_to_utc(dt: datetime) -> datetime:
  if dt is None:
    return None

  if dt.tzinfo is None or dt.utcoffset() is None:
    dt = dt.replace(tzinfo=ZoneInfo('UTC'))

  return dt.astimezone(ZoneInfo('UTC'))

def inspect_day_duration(start: datetime, end: datetime, interval: int) -> bool:
  return abs(end - start) <= timedelta(days=interval)

def inspect_mins_duration(start: datetime, end: datetime, interval: int) -> bool:
  return abs(end - start) <= timedelta(minutes=interval)
