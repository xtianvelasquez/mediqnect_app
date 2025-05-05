from datetime import datetime, timedelta

def inspect_duration(start, end, interval):
  result = (end - start) < timedelta(days=interval)
  return result