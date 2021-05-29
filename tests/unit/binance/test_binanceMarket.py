"""
Test cases for Binance Market APIs.

IMPORTANT!
----------
    In order for it to work, `binance` package has to locally installed.
    I will draft the instruction on how to do it later.

    Don't try it at home without adult supervision!

Date: 2021-05-27
Author: Vitali Lupusor
"""

# Import standard modules
from typing import List

# Import local modules
from binance import Binance  # type: ignore


class TestBinanceServerTime:
    """Test Binance `serverTime` endpoint."""

    def test_serverTime_noParameters(self, binance: Binance):
        """Test function without passing parameters."""
        # Import standard modules
        from datetime import datetime, timedelta

        serverTime = binance.public.serverTime()
        assert datetime.now() - serverTime < timedelta(seconds=2)

    def test_serverTime_withParameters(self, binance: Binance):
        """Test function with parameters."""
        # Import third-party modules
        from pytest import raises

        with raises(TypeError):
            binance.public.serverTime('bnbbtc')


class TestBinanceMarket:
    """Test Binance `exchangeInfo` endpoint."""

    def test_exchangeInfo_noParameters(
        self, binance: Binance, exchangeInfo_keys: List[str]
    ):
        """Test function without passing parameters."""
        exchangeInfo = binance.public.exchangeInfo()
        assert exchangeInfo_keys == sorted(exchangeInfo.keys())

    def test_exchangeInfo_withParameter(
        self, binance: Binance, exchangeInfo_keys: List[str]
    ):
        """Test function with a single parameter."""
        exchangeInfo = binance.public.exchangeInfo('bnbbtc')
        assert exchangeInfo_keys == sorted(exchangeInfo.keys())

    def test_exchangeInfo_withParameters(
        self, binance: Binance, exchangeInfo_keys: List[str]
    ):
        """Test function with multiple parameters."""
        exchangeInfo = binance.public.exchangeInfo('bnbbtc', 'btcusdt')
        assert exchangeInfo_keys == sorted(exchangeInfo.keys())

    def test_exchangeInfo_badSymbol(self, binance: Binance):
        """
        Test function with bad parameters.

        Expect `RequestException`.
        """
        # Import third-party modules
        from json import dumps
        from pytest import raises
        from requests.exceptions import RequestException

        with raises(RequestException) as badRequest:
            binance.public.exchangeInfo('badSymbol')
            expected_response = dumps(
                {
                    "url": (
                        "https://testnet.binance.vision/api/v3/exchangeInfo?"
                        "symbols=%5B%badSymbol%22%5D"
                    ),
                    "status_code": 400,
                    "reason": "Bad Request",
                    "message": '{"code":-1121,"msg":"Invalid symbol."}'
                },
                indent=2
            )
            expected_response in str(badRequest.value)


class TestBinanceOrderBook:
    """Test Binance `depth` endpoint."""

    def test_orderBook_noParameters(self, binance: Binance):
        """
        Test function without passing parameters.

        Expect `TypeError` being raised.
        """
        # Import third-party modules
        from pytest import raises

        with raises(TypeError) as typeError:
            binance.public.orderBook()
            err = (
                "orderBook() missing 1 required positional argument: 'symbol'"
            )
            err in str(typeError.value)

    def test_orderBook_with_symbol(
        self, binance: Binance, orderBook_keys: List[str]
    ):
        """Test function with correct `symbol` and no provided `limit`."""
        orderBook = binance.public.orderBook('bnbbtc')
        assert orderBook_keys == sorted(orderBook.keys())

    def test_orderBook_with_badSymbol(self, binance: Binance):
        """
        Test function with bad `symbol` and no provided `limit`.

        Expect `RequestException`
        """
        # Import third-party modules
        from json import dumps
        from pytest import raises
        from requests.exceptions import RequestException

        with raises(RequestException) as badRequest:
            binance.public.orderBook('badSymbol')
            err = dumps(
                {
                    "url": (
                        "https://testnet.binance.vision/api/v3/depth?symbol="
                        "BADSYMBOL&limit=100"
                    ),
                    "status_code": 400,
                    "reason": "Bad Request",
                    "message": '{"code":-1121,"msg":"Invalid symbol."}'
                }
            )
            err in str(badRequest.value)

    def test_orderBook_with_allParameters(
        self, binance: Binance, orderBook_keys: List[str]
    ):
        """Test function with all correctly provided parameters."""
        orderBook = binance.public.orderBook('bnbbtc', 5)
        assert orderBook_keys == sorted(orderBook.keys())

    # def test_orderBook_with_OutOfRangeLimit(
    #     self, binance: Binance, orderBook_keys: List[str]
    # ):
    #     """TODO: Add description."""
    #     orderBook = binance.public.orderBook('bnbbtc', 5001)


class TestBinanceRecentTrades:
    """Test Binance `trades` endpoint."""

    def test_recentTrades_with_noSymbol(self, binance: Binance):
        """
        Test function without providing `symbol`; and default `limit`.

        Expect `TypeError`.
        """
        # Import third-party modules
        from pytest import raises

        with raises(TypeError) as typeError:
            binance.public.recentTrades()
            err = (
                "recentTrades() missing 1 required positional argument: "
                "'symbol'"
            )
            err in str(typeError.value)

    def test_recentTrades_with_badSymbol(self, binance: Binance):
        """
        Test function with invalid `symbol` and default `limit`.

        Expect `TypeError`.
        """
        # Import third-party modules
        from json import dumps
        from pytest import raises
        from requests.exceptions import RequestException

        with raises(RequestException) as badRequest:
            binance.public.recentTrades('badSymbol')
            err = dumps(
                {
                    "url": (
                        "https://testnet.binance.vision/api/v3/trades?symbol="
                        "BADSYMBOL&limit=500"
                    ),
                    "status_code": 400,
                    "reason": "Bad Request",
                    "message": '{"code":-1121,"msg":"Invalid symbol."}'
                }
            )
            err in str(badRequest.value)

    def test_recentTrades_with_symbol(
        self, binance: Binance, trades_keys: List[str]
    ):
        """Test function with valid `symbol` and default `limit`."""
        recentTrades = binance.public.recentTrades('bnbbtc')
        assert isinstance(recentTrades, list) \
            and trades_keys == sorted(next(iter(recentTrades)).keys())

    def test_recentTrades_with_allParameters(
        self, binance: Binance, trades_keys: List[str]
    ):
        """Test function with correctly provided parameters."""
        recentTrades = binance.public.recentTrades('bnbbtc', 10)
        assert isinstance(recentTrades, list) \
            and trades_keys == sorted(next(iter(recentTrades)).keys())


class TestBinanceTradeLookup:
    """Test Binance `historicalTrades` endpoint."""

    def test_tradeLookup_with_noSymbol(self, binance: Binance):
        """
        Test function without `symbol`; and default `fromId` and `limit`.

        Expect `TypeError`.
        """
        # Import third-party modules
        from pytest import raises

        with raises(TypeError) as typeError:
            binance.public.tradeLookup()
            err = (
                "tradeLookup() missing 1 required positional argument: "
                "'symbol'"
            )
            err in str(typeError.value)

    def test_tradeLookup_with_badSymbol(self, binance: Binance):
        """
        Test function with invalid `symbol` and default `fromId` and `limit`.

        Expect `TypeError`.
        """
        # Import third-party modules
        from json import dumps
        from pytest import raises
        from requests.exceptions import RequestException

        with raises(RequestException) as badRequest:
            binance.public.tradeLookup('badSymbol')
            err = dumps(
                {
                    "url": (
                        "https://testnet.binance.vision/api/v3/"
                        "historicalTrades?symbol=BADSYMBOL&limit=500"
                    ),
                    "status_code": 400,
                    "reason": "Bad Request",
                    "message": '{"code":-1121,"msg":"Invalid symbol."}'
                }
            )
            err in str(badRequest.value)

    def test_tradeLookup_with_symbol(
        self, binance: Binance, trades_keys: List[str]
    ):
        """Test with valid `symbol` and default `fromId` and `limit`."""
        tradeLookup = binance.public.tradeLookup('bnbbtc')
        assert isinstance(tradeLookup, list) \
            and trades_keys == sorted(next(iter(tradeLookup)).keys())

    def test_tradeLookup_with_allParameters(
        self, binance: Binance, trades_keys: List[str]
    ):
        """Test function with all parameters correctly provided."""
        tradeLookup = binance.public.tradeLookup('bnbbtc', 1, 1)
        assert isinstance(tradeLookup, list) \
            and trades_keys == sorted(next(iter(tradeLookup)).keys())


# TODO: Continue from here!


class TestBinanceAggTrades:
    """TODO: Add description."""

    def test_aggTrades(self, binance: Binance):
        """TODO: Add description."""
        aggTrades = binance.public.aggTrades('bnbbtc', limit=1)
        expected_keys = ['M', 'T', 'a', 'f', 'l', 'm', 'p', 'q']
        assert type(aggTrades) == list \
            and expected_keys == sorted(next(iter(aggTrades)).keys())


class TestBinanceKlines:
    """TODO: Add description."""

    def test_klines(self, binance: Binance):
        """TODO: Add description."""
        klines = binance.public.klines('bnbbtc', interval='1d', limit=1)
        assert isinstance(klines, list) and len(next(iter(klines))) == 12


class TestBinanceAveragePrice:
    """TODO: Add description."""

    def test_avgPrice(self, binance: Binance):
        """TODO: Add description."""
        avgPrice = binance.public.avgPrice('bnbbtc')
        expected_keys = ['mins', 'price']
        assert expected_keys == sorted(avgPrice.keys())


class TestBinancePriceTicker24:
    """TODO: Add description."""

    def test_priceTicker24(self, binance: Binance):
        """TODO: Add description."""
        priceTicker24 = binance.public.priceTicker24('bnbbtc')
        expected_keys = [
            'askPrice', 'askQty', 'bidPrice', 'bidQty', 'closeTime', 'count',
            'firstId', 'highPrice', 'lastId', 'lastPrice', 'lastQty',
            'lowPrice', 'openPrice', 'openTime', 'prevClosePrice',
            'priceChange', 'priceChangePercent', 'quoteVolume', 'symbol',
            'volume', 'weightedAvgPrice',
        ]
        assert expected_keys == sorted(priceTicker24.keys())


class TestBinanceCurrentPrice:
    """TODO: Add description."""

    def test_currentPrice(self, binance: Binance):
        """TODO: Add description."""
        currentPrice = binance.public.currentPrice('bnbbtc')
        expected_keys = ['price', 'symbol']
        assert expected_keys == sorted(currentPrice.keys())


class TestBinanceBookTicker:
    """TODO: Add description."""

    def test_bookTicker(self, binance: Binance):
        """TODO: Add description."""
        bookTicker = binance.public.bookTicker('bnbbtc')
        expected_keys = ['askPrice', 'askQty', 'bidPrice', 'bidQty', 'symbol']
        assert expected_keys == sorted(bookTicker.keys())
