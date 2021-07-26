"""
Date: 2021
Author: Barry Foye
"""
import datetime
import time
from typing import Dict
INTERVALS = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
TODAY_MINUS_SEVEN = 6
TODAY_MINUS_SIXTY = 59
TODAY_MINUS_SEVEN_THIRTY = 729


def rate_limiter(limit: float = None) -> None:
    """
    Limits the rate at which a function can be called.

    These limits are usually enforced by the API provider.
    """
    if limit is None:
        time.sleep(1.818)  # 1.818 specific to yahoo rate limits
    else:
        time.sleep(limit)
    pass


def date_range(interval: str = None) -> Dict:
    """
    Return a date range and the given interval for the yfinance api.

    If a range is not needed it will return a period = to max.
    It also returns an error if it gets the worng data.

    The lower time intervals have specific restrictions, so simply calling
    the interval with 'max' will throw an error relating to the limitation.

    Example usage:
    in: date_range('1m')
    out: {'start': '2021-07-20', 'end': '2021-07-26', 'interval': '1m'}

    Return values:
    {'period': 'max', 'interval': 'null'}
    {'start': '2021-07-20', 'end': '2021-07-26', 'interval': '1m'}
    {'start': '2021-05-28', 'end': '2021-07-26', 'interval': '2m'}
    {'start': '2021-05-28', 'end': '2021-07-26', 'interval': '5m'}
    {'start': '2021-05-28', 'end': '2021-07-26', 'interval': '15m'}
    {'start': '2021-05-28', 'end': '2021-07-26', 'interval': '30m'}
    {'start': '2019-07-28', 'end': '2021-07-26', 'interval': '60m'}
    {'start': '2021-05-28', 'end': '2021-07-26', 'interval': '90m'}
    {'start': '2019-07-28', 'end': '2021-07-26', 'interval': '1h'}
    {'period': 'max', 'interval': '1d'}
    {'period': 'max', 'interval': '5d'}
    {'period': 'max', 'interval': '1wk'}
    {'period': 'max', 'interval': '1mo'}
    {'period': 'max', 'interval': '3mo'}
    """
    # Gets 7 days previous which is the max for the API
    seven = ['1m']
    # Gets 60 days previous which is the max for the API
    sixty = ['2m', '5m', '15m', '30m', '90m']
    # Gets 730 days previous which is the max for the API
    seven_three_zero = ['60m', '1h']
    start_s = None
    look_back = None
    interval_ = interval
    if interval not in INTERVALS:
        return {'error': f'{interval} is invalid', 'allowed_values': INTERVALS}
    elif interval in seven:
        start_s = datetime.datetime.strptime(
            time.ctime(float(time.time())), "%a %b %d %H:%M:%S %Y"
            )
        look_back = start_s - datetime.timedelta(days=TODAY_MINUS_SEVEN)
    elif interval in sixty:
        start_s = datetime.datetime.strptime(
            time.ctime(float(time.time())), "%a %b %d %H:%M:%S %Y"
            )
        look_back = start_s - datetime.timedelta(days=TODAY_MINUS_SIXTY)
    elif interval in seven_three_zero:
        start_s = datetime.datetime.strptime(
            time.ctime(float(time.time())), "%a %b %d %H:%M:%S %Y"
            )
        look_back = start_s - datetime.timedelta(days=TODAY_MINUS_SEVEN_THIRTY)
    else:
        return {'period': 'max', 'interval': interval_}
    return {
        'start': look_back.strftime('%Y-%m-%d'),
        'end': start_s.strftime('%Y-%m-%d'),
        'interval': interval_
        }


if __name__ == '__main__':
  intervals = ['null', '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
  for interval in intervals:
    print(date_range(interval))
  pass