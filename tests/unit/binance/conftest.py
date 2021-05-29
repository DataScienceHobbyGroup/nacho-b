"""
PyTest configuration.

Date: 2021-05-29
Author: Vitali Lupusor
"""

# Import standard modules
from typing import List

# Import third-party modules
from pytest import fixture

# Import local modules
from binance import Binance  # type: ignore


@fixture(scope='session')
def binance() -> Binance:
    """
    Instantiate `Binance` class.

    This object will be used throughout the testing of Binance API SDK.

    Currently, the API key and secret are sourced from a `.env` file.
    Since `.env` files are not being uploaded to project repositories, this
    has to change to sourcing the parameters from a vault.
    """
    dotenv = '.env'  # Relative path to `.env` file
    binance = Binance.from_env_file(dotenv)

    return binance


@fixture
def exchangeInfo_keys() -> List[str]:
    """Expect below keys as result of `exchengeInfo` API endpoint call."""
    return [
        'exchangeFilters', 'rateLimits', 'serverTime', 'symbols', 'timezone',
    ]


@fixture
def orderBook_keys() -> List[str]:
    """Expect below keys as result of `depth` API endpoint call."""
    return ['asks', 'bids', 'lastUpdateId']


@fixture
def trades_keys() -> List[str]:
    """
    Expect below keys as result of trade-related API endpoints calls.

    Endpoints:
        - `trades`
        - `historicalTrades`
    """
    return [
        'id', 'isBestMatch', 'isBuyerMaker', 'price', 'qty', 'quoteQty', 'time'
    ]
