from datetime import date, time, datetime, timedelta
from zoneinfo import ZoneInfo

def convert_to_datetime(d: date) -> datetime:
  if isinstance(d, datetime):
    return d  # already datetime
  if isinstance(d, date):
    return datetime.combine(d, time(hour=23, minute=59, second=0)).replace(tzinfo=ZoneInfo('UTC'))

def convert_to_utc(dt: datetime) -> datetime:
  if dt.tzinfo is None or dt.utcoffset() is None:
    raise ValueError('Datetime must be timezone-aware')

  return dt.astimezone(ZoneInfo('UTC'))

def inspect_duration(start, end, interval):
  result = (end - start) < timedelta(days=interval)
  return result
