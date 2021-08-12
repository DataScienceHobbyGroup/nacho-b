"""
TODO: Add description.

Date: 2021-05-23
Author: Vitali Lupusor
"""

# Import standard modules
from typing import Any, Union


def sign(secret: Union[bytes, str], **params: Any) -> dict:
    """
    Create a `timestamp` based HMAC signature.

    Parameters
    ----------
        secret (Union[bytes, str]):
            Binance API secret.

    Returns
    -------
        (dict)
        Request parameters with `HMAC` signature.
    """
    # Import standard modules
    import hmac
    from datetime import datetime
    from urllib.parse import urlencode

    # Configure default parameters
    _secret = secret if isinstance(secret, bytes) else secret.encode('utf-8')

    # Get rid of parameters with no values
    _params = {
        key: value for key, value in params.items() if value
    }

    if 'recvWindow' not in _params:
        _params['recvWindow'] = 5000  # milliseconds
    _params['timestamp'] = int(
        datetime.timestamp(datetime.now()) * 1000  # Convert to milliseconds
    )

    signature = urlencode(_params)
    _signature = hmac.new(
        key=_secret,
        msg=signature.encode('utf-8'),
        digestmod='sha256'
    ).hexdigest()
    _params['signature'] = _signature

    return _params


del(Any, Union)
