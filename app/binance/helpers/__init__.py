"""
Collection of helper functions.

Date: 2021-05-20
Author: Vitali Lupusor
"""

# Import standard modules
from datetime import date, datetime
from typing import Any, Optional, Union


def get(
    url: str,
    endpoint: str,
    key: Optional[str] = None,
    secret: Optional[str] = None,
    **params: Any
) -> Any:
    """
    TODO: Add description.

    Parameters
    ----------
        url (str):
            Server URL.

        endpoint (str):
            Server endpoint for the API call.

        key (Optional[str]):
            Binance API key.
            Defaults to ``None``.

        secret (Optional[str]):
            Binance API secret.
            Defaults to ``None``.

        **params (Any):
            symbol (str):
                Currency symbol.

            limit (int):
                TODO: Add description.

            side (Literal['BUY', 'SELL']):
                TODO: Add description.

            type (TODO: Add type):
                TODO: Add description.

            timeInForce (TODO: Add type):
                TODO: Add description.

            quantity (float):
                TODO: Add description.

            price (float):
                TODO: Add description.

            recvWindow (int):
                Number of milliseconds in which to complete the transaction.
                If timeout, transaction is being cancelled.
                Defaults to 5000.

    Returns
    -------
        (Any)
        TODO: Add description.
    """
    # Import local modules
    from .requests import request

    return request('get', url, endpoint, key, secret, **params)


def post(
    url: str,
    endpoint: str,
    key: Optional[str] = None,
    secret: Optional[str] = None,
    **params: Any
) -> Any:
    """
    TODO: Add description.

    Parameters
    ----------
        url (str):
            Server URL.

        endpoint (str):
            Server endpoint for the API call.

        key (Optional[str]):
            Binance API key.
            Defaults to ``None``.

        secret (Optional[str]):
            Binance API secret.
            Defaults to ``None``.

        **params (Any):
            symbol (str):
                Currency symbol.

            limit (int):
                TODO: Add description.

            side (Literal['BUY', 'SELL']):
                TODO: Add description.

            type (TODO: Add type):
                TODO: Add description.

            timeInForce (TODO: Add type):
                TODO: Add description.

            quantity (float):
                TODO: Add description.

            price (float):
                TODO: Add description.

            recvWindow (int):
                Number of milliseconds in which to complete the transaction.
                If timeout, transaction is being cancelled.
                Defaults to 5000.

    Returns
    -------
        (Any)
        TODO: Add description.
    """
    # Import local modules
    from .requests import request

    return request('post', url, endpoint, key, secret, **params)


def to_timestamp(
    value: Union[str, date, datetime],
    datetime_format: Optional[str] = None
) -> int:
    """
    Convert date/datetime object or thereof string representation to timestamp.

    The timestamp is the equal to the number of milliseconds passed since
    ``1990-01-01 00:00:00``.

    Parameters
    ----------
        value (Union[str, datetime.date, datetime.datetime]):
            Date/datetime object or thereof string representation

        datetime_format (str):
            If ``value`` is provided as a string representation of
            ``datetime``, a pythonic datetime format string can be provided.
            Example: '%Y-%m-%d %H:%M:%S' for UTC datetime format
            (2021-01-01 00:00:00).
            If not provided, the function will attempt to autodetect the
            format. Defaults to ``None``.

    Returns
    -------
        (int)
        Timestamp in milliseconds instance of the provided ``value``.
    """
    if not datetime_format:
        date_parts = ['%Y-%m-%d', '%d-%m-%Y']
        time_parts = [' %H:%M:%S', 'T%H:%M:%S', "'T'%H:%M:%S"]
        offset_parts = ['', '.%f', '%z', ' %Z', '.%f%z', '.%f %Z']
        validFormats = [
            date_part+time_offset_part for date_part in date_parts
            for time_offset_part in ['']+[
                time_part+offset_part for time_part in time_parts
                for offset_part in offset_parts
            ]
        ]
    else:
        validFormats = [datetime_format]

    if isinstance(value, str):
        for strformat in validFormats:
            try:
                value = datetime.strptime(value, strformat)  # type: ignore
            except ValueError:
                pass
            else:
                break

    return int(datetime.timestamp(value)*1000)  # type: ignore


del(Any, Optional, Union, date)