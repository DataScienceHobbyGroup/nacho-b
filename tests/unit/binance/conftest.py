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
def symbol() -> str:
    """Define the `symbol` parameter used throughout test suit."""
    return 'bnbbtc'


@fixture
def badSymbol() -> str:
    """Define invalid `symbol` parameter used throughout test suit."""
    return 'badSymbol'


@fixture
def limit() -> str:
    """Define the `limit` parameter used throughout test suit."""
    return 10


@fixture
def interval() -> str:
    """Define the `interval` parameter used throughout test suit."""
    return '1w'


@fixture
def buySide() -> str:
    """TODO: Add description."""
    return 'BUY'


@fixture
def sellSide() -> str:
    """TODO: Add description."""
    return 'SELL'


@fixture
def trade_type() -> str:
    """TODO: Add description."""
    return 'MARKET'


@fixture
def quantity() -> float:
    """TODO: Add description."""
    return 1.


@fixture
def recvWindow() -> int:
    """TODO: Add description."""
    return 2000


@fixture
def timeInForce() -> str:
    """TODO: Add description."""
    return 'GTC'


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


@fixture
def aggTrades_keys() -> List[str]:
    """Expect below keys as result of `aggTrades` API endpoint call."""
    return ['M', 'T', 'a', 'f', 'l', 'm', 'p', 'q']
