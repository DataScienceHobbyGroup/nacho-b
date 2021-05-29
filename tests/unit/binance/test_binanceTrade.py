"""
Test cases for Binance Trade APIs.

IMPORTANT!
----------
    In order for it to work, `binance` package has to locally installed.
    I will draft the instruction on how to do it later.

    Don't try it at home without adult supervision!

Date: 2021-05-29
Author: Vitali Lupusor
"""

# Import local modules
from binance import Binance  # type: ignore

dotenv = '.env'  # Relative path to `.env` file
binance = Binance.from_env_file(dotenv)


class TestBinanceTrade:
    """TODO: Add description."""

    def test_order(self):
        """TODO: Add description."""
        ...

    def test_testOrder(self):
        """TODO: Add description."""
        ...

    def test_myTrades(self):
        """TODO: Add description."""
        ...

    def test_cancelOrder(self):
        """TODO: Add description."""
        ...

    def test_cancelAllOpenOrders(self):
        """TODO: Add description."""
        ...

    def test_queryOrder(self):
        """TODO: Add description."""
        ...

    def test_openOrders(self):
        """TODO: Add description."""
        ...
