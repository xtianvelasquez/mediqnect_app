from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def convert_datetime(dt: datetime) -> str:
  if dt is None:
    return None

  if dt.tzinfo is None or dt.utcoffset() is None:
    dt = dt.replace(tzinfo=ZoneInfo('UTC'))

  local_dt = dt.astimezone(ZoneInfo('Asia/Manila'))

  return local_dt.strftime('%Y-%m-%d %H:%M')

def convert_to_utc(dt: datetime) -> datetime:
  if dt is None:
    return None

  if dt.tzinfo is None or dt.utcoffset() is None:
    dt = dt.replace(tzinfo=ZoneInfo('UTC'))

  return dt.astimezone(ZoneInfo('UTC'))

def convert_to_tz(dt: datetime) -> datetime:
  manila_tz = ZoneInfo('Asia/Manila')
  return dt.replace(tzinfo=manila_tz) if dt.tzinfo is None else dt.astimezone(manila_tz)

def count_datetime_gap(start: datetime, end: datetime) -> int:
  return int(abs((end - start).total_seconds()) // 60)

def inspect_day_duration(start: datetime, end: datetime, interval: int) -> bool:
  return abs(end - start) <= timedelta(days=interval)

def inspect_mins_duration(start: datetime, end: datetime, interval: int) -> bool:
  return abs(end - start) <= timedelta(minutes=interval)
