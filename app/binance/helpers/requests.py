"""
TODO: Add description.

Date: 2021-05-23
Author: Vitali Lupusor
"""

# Import standard modules
from requests import Response
from typing import Any, Callable, Literal, Optional, Union


def response_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    """TODO: Add description."""
    # Import standard modules
    from functools import wraps

    @wraps(func)
    def wrapper_response_handler(
        *args: Any, **kwargs: Any
    ) -> Union[dict, list]:
        """TODO: Add description.

        Parameters
        ----------
            url (str):
                Server URL.

            endpoint (str):
                Server endpoint for the API call.

            key Optional[str]:
                Binance API key.
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
                    Number of milliseconds to complete the transaction.
                    If timeout, transaction is being cancelled.
                    Defaults to 5000.

        Raises
        ------
            requests.exceptions.RequestException
                When bad request provided.

        Returns
        -------
            (Union[dict, list])
            TODO: Add description.
        """
        # Import standard modules
        import json
        from requests.exceptions import RequestException

        response = func(*args, **kwargs)

        if not response.ok:
            err = json.dumps(
                {
                    'url': response.url,
                    'status_code': response.status_code,
                    'reason': response.reason,
                    'message': response.content.decode('utf-8')
                },
                indent=2
            )
            raise RequestException(err)

        return response.json()

    return wrapper_response_handler


@response_handler
def request(
    method: Literal['get', 'delete', 'post', 'put'],
    url: str,
    endpoint: str,
    key: Optional[str] = None,
    secret: Optional[str] = None,
    **params: Any
) -> Response:
    """
    TODO: Add description.

    Parameters
    ----------
        url (str):
            Server URL.

        endpoint (str):
            Server endpoint for the API call.

        key Optional[str]:
            Binance API key.
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
        (requests.models.Response)
        TODO: Add description.
    """
    # Import standard modules
    import requests

    # Import local modules
    from .sign_request import sign

    # Configure parameters
    _url = '/'.join([url, endpoint])
    _headers = {'X-MBX-APIKEY': key} if key else None
    _params = params

    if secret:
        _params = sign(secret, **params)

    return requests.request(method, url=_url, headers=_headers, params=_params)


del(Callable, Literal, Response)
