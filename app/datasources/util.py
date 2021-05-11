import datetime
import time
from typing import Dict
INTERVALS = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
TODAY_MINUS_SEVEN = 6
TODAY_MINUS_SIXTY = 59
TODAY_MINUS_SEVEN_THIRTY = 729

def rate_limiter(limit:float=None) -> None:
  if limit == None:
    time.sleep(1.818) # 1.818 specific to yahoo rate limits
  else:
    time.sleep(limit)
  pass
# Returns a date range and the given interval for the yfinance api. 
# If a range is not needed it will return a period = to max.
# It also returns an error if it gets the worng data
def date_range(interval:str=None) -> Dict:
  seven = ['1m']
  sixty = ['2m', '5m', '15m', '30m', '90m']
  seven_three_zero = ['60m', '1h']
  start_s = None
  look_back = None
  interval_ = interval
  if interval not in INTERVALS:
    return {'error': f'{interval} is invalid', 'allowed_values': INTERVALS}
  elif interval in seven:
    start_s = datetime.datetime.strptime(time.ctime(float(time.time())), "%a %b %d %H:%M:%S %Y")
    look_back = start_s - datetime.timedelta(days=TODAY_MINUS_SEVEN)
  elif interval in sixty:
    start_s = datetime.datetime.strptime(time.ctime(float(time.time())), "%a %b %d %H:%M:%S %Y")
    look_back = start_s - datetime.timedelta(days=TODAY_MINUS_SIXTY)
  elif interval in seven_three_zero:
    start_s = datetime.datetime.strptime(time.ctime(float(time.time())), "%a %b %d %H:%M:%S %Y")
    look_back = start_s - datetime.timedelta(days=TODAY_MINUS_SEVEN_THIRTY)
  else:
    return {'period': 'max', 'interval': interval_}
  return {'start': look_back.strftime('%Y-%m-%d'), 'end': start_s.strftime('%Y-%m-%d'), 'interval': interval_}

if __name__ == '__main__':
  intervals = ['null', '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
  for interval in intervals:
    print(date_range(interval))
  pass