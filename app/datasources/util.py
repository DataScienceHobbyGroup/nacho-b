import re
import datetime
import time
import math
from typing import List, Dict
pattern = 'startTime+=([0-9]+)'
SECONDS_TO_DAYS = 86400
SEVEN_DAYS = 7
# The yahoo finance api only returns 7 days of 1 minute data ata a time.
# Therefore we need to first capture the starting point for each ticker
# as Yahoo has not got the same starting point for each.
# Luckily enough if we call for the one minute data entirely then we get
# a helpful message back telling us the original start date amongst other
# information. We need to parse this error and extract the start date. We
# then need to create a list of start and end dates spaced ~7 days apart
# and feed it back to the algorithm to make requests for the right start
# and end periods. We also need to consider the API call limitations which
# are 2000 per hour or 48,000 per day. For example (as of 07/05/2021) 
# BTC-USD has 2424 days of data. Thats 2424/7(limit) or ~347 API calls.
# There are ~3,000 symbols. If we take worst case, they all have ~347 
# API calls thats ~3,000 x ~347 = ~1.05mm calls. So it would take ~520 
# hours or ~22 daysto get the entire set. The utility should provide a 
# parsing method for the start date, a time calculation method for 
# returning a list of time periods to request and a limitation function
# to help ensure the system does not go over the rate limit.

def parse_historical_start_date(errorMsg:str) -> str:
  return (re.findall(pattern, errorMsg))[0]

def calculate_time_periods_for_ticker(startDate:str):
  start_s = datetime.datetime.strptime(time.ctime(float(startDate)), "%a %b %d %H:%M:%S %Y")
  now = time.time()
  duration_in_seconds = now - float(startDate)
  weekly_steps = math.floor((duration_in_seconds/SECONDS_TO_DAYS)/SEVEN_DAYS)
  date_ranges = []
  # get incremental time periods
  for i in range(weekly_steps):
    date_ranges.append({'start': start_s, 'end': start_s + datetime.timedelta(days=6) })
    start_s = start_s + datetime.timedelta(days=7)
  #convert to API expected input (example: 2017-01-01)
  for range_ in date_ranges:
    range_["start"] = range_["start"].strftime('%Y-%m-%d')
    range_["end"]  = range_["end"].strftime('%Y-%m-%d')
  return date_ranges

def rate_limiter(limit:float=None) -> None:
  if limit == None:
    time.sleep(1.818)
  else:
    time.sleep(limit)
  pass

if __name__ == '__main__':
  ps = parse_historical_start_date('- BTC-USD: 1m data not available for startTime=1410908400 and endTime=1620417497. Only 7 days worth of 1m granularity data are allowed to be fetched per request.')
  dr = calculate_time_periods_for_ticker(ps)
  pass