"""
Test suit for Binance helper functions.

Date: 2021-05-30
Author: Vitali Lupusor
"""


def test_to_timestamp():
    """
    Test `to_timestamp` helper function.

    The function transforms `date`, `datetime` and `str` representation of
    dates into millisecond-precision timestamp.
    """
    # Import standard modules
    from datetime import datetime

    # Import local modules
    from binance.helpers import to_timestamp

    str_datetime = '1990-01-01 00:00:00'
    str_timeFormat = '%Y-%m-%d %H:%M:%S'
    test_timestamp = to_timestamp(str_datetime, str_timeFormat)
    timestamp = datetime.timestamp(
        datetime.strptime(str_datetime, str_timeFormat)
    ) * 1000

    assert timestamp == test_timestamp
