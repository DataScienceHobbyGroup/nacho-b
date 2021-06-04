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


class TestBinanceTestOrder:
    """TODO: Add description."""

    def test_testOrder_with_noParameters(self, binance: Binance):
        """
        Test function without mandatory parameters.

        Expect `TypeError`.
        """
        # Import third-party modules
        from pytest import raises

        with raises(TypeError) as typeError:
            binance.trade.testOrder()

            err = (
                'testOrder() missing 3 required positional arguments: '
                "'symbol', 'side', and 'type'"
            )
            err in str(typeError.value)

    def test_buyTestOrder_with_validParameters(
        self, binance: Binance, symbol: str, buySide: str, trade_type: str,
        quantity: float
    ):
        """TODO: Add description."""
        testOrder = binance.trade.testOrder(
            symbol, buySide, trade_type, quantity=quantity
        )
        assert testOrder == {}

    def test_sellTestOrder_with_validParameters(
        self, binance: Binance, symbol: str, sellSide: str, trade_type: str,
        quantity: float, recvWindow: int
    ):
        """TODO: Add description."""
        testOrder = binance.trade.testOrder(
            symbol, sellSide, trade_type, quantity=quantity,
            recvWindow=recvWindow
        )
        assert testOrder == {}


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
