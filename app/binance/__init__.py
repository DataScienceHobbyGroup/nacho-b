"""
Binance API calls.

| Spot API URL                         |               Spot Test Network URL |
| :----------------------------------- | ----------------------------------: |
| https://api.binance.com/api          | https://testnet.binance.vision/api  |
| wss://stream.binance.com:9443/ws     | wss://testnet.binance.vision/ws     |
| wss://stream.binance.com:9443/stream | wss://testnet.binance.vision/stream |

Date: 2021-05-16
Author: Vitali Lupusor
"""

# Import standard modules
from dotenv import load_dotenv
from typing import Any, Callable, Optional

# Import local modules
from .methods.market import Get
from .methods.client import Trade

load_dotenv('.env')


class Binance:
    """Binance APIs interaction object."""

    def __init__(
        self,
        key: Optional[str] = None,
        secret: Optional[str] = None,
        url: Optional[str] = None
    ) -> None:
        """
        Binance client.

        Parameters
        ----------
            key (Optional[str]):
                API key required to interact with certain functionalities of
                the server. Defaults to None.

            secret (Optional[str]):
                TODO: Add description.
                Defaults to None.

            url (str):
                Server URL.
                Defaults to ``https://testnet.binance.vision/api/v3``.

        Arguments
        ---------
            get (Callable[..., Any]):
                Object for calling on ``Market Data Endpoints`` Binance APIs.

            trade (Callable[..., Any]):
                Object for calling on ``Spot Account/Trade`` Binance APIs.

            url (str):
                Server URL where the requests will be sent to.
        """
        # Import standard modules
        from os import getenv

        self.__key = key or getenv('API_KEY')
        self.__secret = secret or getenv('API_SECRET')
        self._url = url or 'https://testnet.binance.vision/api/v3'
        self._get = None
        self._trade = None

    def __repr__(self) -> str:
        """Configure object representation."""
        return f'<Binance: {self._url}>'

    @classmethod
    def from_env_file(cls, path: str) -> Callable[..., Any]:
        """
        Load credentials from ``.env`` file.

        Parameters
        ----------
            path (str):
                Path to the ``.env`` file containing the credentials.

        Returns
        -------
            (Callable[..., Any])
            The class itself with API key and secret loaded.
        """
        # Import standard modules
        from os import getenv

        load_dotenv(path)

        key = getenv('API_KEY')
        secret = getenv('API_SECRET')
        url = getenv('API_URL')

        if not all([key, secret]):
            err = (
                '``API_KEY`` and ``API_SECRET`` are mandatory attributes.\n'
                'Please make sure they are contained in your ``.env`` file'
            )
            raise KeyError(err)

        return cls(key, secret, url)

    @classmethod
    def from_json_file(cls, path: str) -> Callable[..., Any]:
        """
        Load credentials from a ``JSON`` file.

        Parameters
        ----------
            path (str):
                Path to the ``JSON`` file containing the credentials.

        Returns
        -------
            (Callable[..., Any])
            The class itself with API key and secret loaded.
        """
        # Import standard modules
        import json

        with open(path) as file_obeject:
            credentials = json.load(file_obeject)

        key = credentials.get('API_KEY')
        secret = credentials.get('API_SECRET')
        url = credentials.get('URL')

        if not all([key, secret]):
            err = (
                '``API_KEY`` and ``API_SECRET`` are mandatory attributes.\n'
                'Please make sure they are contained in your ``.json`` file'
            )
            KeyError(err)

        return cls(key, secret, url)

    @property
    def url(self):
        """Get Binance API URL."""
        return self._url

    @url.setter
    def url(self, url: str):
        """
        Amend Binance API URL.

        Parameters
        ----------
            url (str):
                New Binance API URL.
        """
        self._url = url

    @property
    def get(self):
        """Return all ``GET`` method APIs."""
        if not self._get:
            self._get = Get(self.__key, self._url)
        return self._get

    @property
    def trade(self):
        """Return all ``POST`` method APIs."""
        if not self._trade:
            self._trade = Trade(self.__key, self.__secret, self._url)
        return self._trade


del(Any, Callable, Optional)
