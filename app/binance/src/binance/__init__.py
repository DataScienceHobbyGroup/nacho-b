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
from typing import Optional

# Import local modules
from .api_calls.market import MarketData    # type: ignore
from .api_calls.client import Trade         # type: ignore


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
                Defaults to `https://testnet.binance.vision/api/v3`.

        Arguments
        ---------
            get (MarketData):
                Object for calling on `Market Data Endpoints` Binance APIs.

            trade (Trade):
                Object for calling on `Spot Account/Trade` Binance APIs.

            url (str):
                Server URL where the requests will be sent to.

        """
        # Import standard modules
        from os import getenv

        self.__key = key or getenv('API_KEY')
        self.__secret = secret or getenv('API_SECRET')
        self._url = url or 'https://testnet.binance.vision/api/v3'
        self._public = None
        self._trade = None

    def __repr__(self) -> str:
        """Configure object representation."""
        return f'<Binance: {self._url}>'

    @classmethod
    def from_env_file(cls, filename: str):
        """
        Load credentials from `.env` file.

        Parameters
        ----------
            filename (str):
                Path to the `.env` file containing the credentials.

        Raises
        ------
            FileNotFoundError
                If provided path to `.env` file (`filename`) does not exist.

            KeyError
                If `API_KEY` and `API_SECRET` keys are not present in the
                `.env` file (`filename`).
        """
        # Import standard modules
        from dotenv import load_dotenv
        from os import getenv, path

        # Validate `path`
        if not path.isfile(filename):
            err = f"No such file or directory: '{filename}'"
            raise FileNotFoundError(err)

        load_dotenv(filename)

        key = getenv('API_KEY')
        secret = getenv('API_SECRET')
        url = getenv('API_URL')

        if not all([key, secret]):
            err = (
                '`API_KEY` and `API_SECRET` are mandatory attributes.\n'
                'Please make sure they are contained in your `.env` file'
            )
            raise KeyError(err)

        return cls(key, secret, url)

    @classmethod
    def from_json_file(cls, filename: str):
        """
        Load credentials from a `JSON` file.

        Parameters
        ----------
            filename (str):
                Path to the `JSON` file containing the credentials.

        Raises
        ------
            FileNotFoundError
                If provided path to `.json` format file (`filename`) does not
                exist.

            KeyError
                If `API_KEY` and `API_SECRET` keys are not present in the
                `.json` format file (`filename`).
        """
        # Import standard modules
        from json import load

        with open(filename) as file_obeject:
            credentials = load(file_obeject)

        key = credentials.get('API_KEY')
        secret = credentials.get('API_SECRET')
        url = credentials.get('URL')

        if not all([key, secret]):
            err = (
                '`API_KEY` and `API_SECRET` are mandatory attributes.\n'
                'Please make sure they are contained in your `.json` file'
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
    def public(self) -> MarketData:
        """Return all `Market Data Endpoint` APIs."""
        if not self._public:
            self._public = MarketData(self.__key, self._url)
        return self._public

    @property
    def trade(self) -> Trade:
        """Return all `Spot Account/Trade` APIs."""
        if not self._trade:
            self._trade = Trade(self.__key, self.__secret, self._url)
        return self._trade


del(Optional, )
