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

    def test_serverTime_withParameters(self, binance: Binance, symbol: str):
        """Test function with parameters."""
        # Import third-party modules
        from pytest import raises

        with raises(TypeError):
            binance.public.serverTime(symbol)


class TestBinanceMarket:
    """Test Binance `exchangeInfo` endpoint."""

    def test_exchangeInfo_noParameters(
        self, binance: Binance, exchangeInfo_keys: List[str]
    ):
        """Test function without passing parameters."""
        exchangeInfo = binance.public.exchangeInfo()
        assert exchangeInfo_keys == sorted(exchangeInfo.keys())

    def test_exchangeInfo_withParameter(
        self, binance: Binance, exchangeInfo_keys: List[str], symbol: str
    ):
        """Test function with a single parameter."""
        exchangeInfo = binance.public.exchangeInfo(symbol)
        assert exchangeInfo_keys == sorted(exchangeInfo.keys())

    def test_exchangeInfo_withParameters(
        self, binance: Binance, exchangeInfo_keys: List[str]
    ):
        """Test function with multiple parameters."""
        exchangeInfo = binance.public.exchangeInfo('bnbbtc', 'btcusdt')
        assert exchangeInfo_keys == sorted(exchangeInfo.keys())

    def test_exchangeInfo_badSymbol(self, binance: Binance, badSymbol: str):
        """
        Test function with bad parameters.

        Expect `RequestException`.
        """
        # Import standard modules
        from json import dumps

        # Import third-party modules
        from pytest import raises
        from requests.exceptions import RequestException

        with raises(RequestException) as badRequest:
            binance.public.exchangeInfo(badSymbol)
            expected_response = dumps(
                {
                    "url": (
                        "https://testnet.binance.vision/api/v3/exchangeInfo?"
                        f"symbols=%5B%{badSymbol}%22%5D"
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
        self, binance: Binance, orderBook_keys: List[str], symbol: str
    ):
        """Test function with correct `symbol` and default `limit`."""
        orderBook = binance.public.orderBook(symbol)
        assert orderBook_keys == sorted(orderBook.keys())

    def test_orderBook_with_badSymbol(self, binance: Binance, badSymbol: str):
        """
        Test function with bad `symbol` and default `limit`.

        Expect `RequestException`
        """
        # Import standard modules
        from json import dumps

        # Import third-party modules
        from pytest import raises
        from requests.exceptions import RequestException

        with raises(RequestException) as badRequest:
            binance.public.orderBook(badSymbol)
            err = dumps(
                {
                    "url": (
                        "https://testnet.binance.vision/api/v3/depth?symbol="
                        f"{badSymbol.upper()}&limit=100"
                    ),
                    "status_code": 400,
                    "reason": "Bad Request",
                    "message": '{"code":-1121,"msg":"Invalid symbol."}'
                }
            )
            err in str(badRequest.value)

    def test_orderBook_with_allParameters(
        self, binance: Binance, orderBook_keys: List[str], symbol: str,
        limit: int
    ):
        """Test function with all correctly provided parameters."""
        orderBook = binance.public.orderBook(symbol, limit)
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

    def test_recentTrades_with_badSymbol(
        self, binance: Binance, badSymbol: str
    ):
        """
        Test function with invalid `symbol` and default `limit`.

        Expect `TypeError`.
        """
        # Import standard modules
        from json import dumps

        # Import third-party modules
        from pytest import raises
        from requests.exceptions import RequestException

        with raises(RequestException) as badRequest:
            binance.public.recentTrades(badSymbol)
            err = dumps(
                {
                    "url": (
                        "https://testnet.binance.vision/api/v3/trades?symbol="
                        f"{badSymbol.upper()}&limit=500"
                    ),
                    "status_code": 400,
                    "reason": "Bad Request",
                    "message": '{"code":-1121,"msg":"Invalid symbol."}'
                }
            )
            err in str(badRequest.value)

    def test_recentTrades_with_symbol(
        self, binance: Binance, trades_keys: List[str], symbol: str
    ):
        """Test function with valid `symbol` and default `limit`."""
        recentTrades = binance.public.recentTrades(symbol)
        assert isinstance(recentTrades, list) \
            and trades_keys == sorted(next(iter(recentTrades)).keys())

    def test_recentTrades_with_allParameters(
        self, binance: Binance, trades_keys: List[str], symbol: str, limit: int
    ):
        """Test function with correctly provided parameters."""
        recentTrades = binance.public.recentTrades(symbol, limit)
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

    def test_tradeLookup_with_badSymbol(
        self, binance: Binance, badSymbol: str
    ):
        """
        Test function with invalid `symbol` and default `fromId` and `limit`.

        Expect `TypeError`.
        """
        # Import standard modules
        from json import dumps

        # Import third-party modules
        from pytest import raises
        from requests.exceptions import RequestException

        with raises(RequestException) as badRequest:
            binance.public.tradeLookup(badSymbol)
            err = dumps(
                {
                    "url": (
                        "https://testnet.binance.vision/api/v3/"
                        f"historicalTrades?symbol={badSymbol.upper()}"
                        "&limit=500"
                    ),
                    "status_code": 400,
                    "reason": "Bad Request",
                    "message": '{"code":-1121,"msg":"Invalid symbol."}'
                }
            )
            err in str(badRequest.value)

    def test_tradeLookup_with_symbol(
        self, binance: Binance, trades_keys: List[str], symbol: str
    ):
        """Test with valid `symbol` and default `fromId` and `limit`."""
        tradeLookup = binance.public.tradeLookup(symbol)
        assert isinstance(tradeLookup, list) \
            and trades_keys == sorted(next(iter(tradeLookup)).keys())

    def test_tradeLookup_with_allParameters(
        self, binance: Binance, trades_keys: List[str], symbol: str, limit: int
    ):
        """Test function with all parameters correctly provided."""
        tradeLookup = binance.public.tradeLookup(symbol, limit, 1)
        assert isinstance(tradeLookup, list) \
            and trades_keys == sorted(next(iter(tradeLookup)).keys())


class TestBinanceAggTrades:
    """Test suit for `aggTrades` Binance API endpoint."""

    def test_aggTrades_with_noParametrs(self, binance: Binance):
        """
        Test function without mandatory parameters.

        Expect `TypeError`.
        """
        # Import third-party modules
        from pytest import raises

        with raises(TypeError) as typeError:
            binance.public.aggTrades()
            err = (
                "aggTrades() missing 1 required positional argument: "
                "'symbol'"
            )
            err in str(typeError.value)

    def test_aggTrades_with_symbol(
        self, binance: Binance, aggTrades_keys: List[str], symbol: str
    ):
        """Test function with valid mandatory parameters."""
        aggTrades = binance.public.aggTrades(symbol)
        assert type(aggTrades) == list \
            and aggTrades_keys == sorted(next(iter(aggTrades)).keys())

    def test_aggTrades_with_badSymbol(
        self, binance: Binance, badSymbol: str
    ):
        """
        Test function with invalid `symbol` and default optional parameters.

        Expect `RequestException`.
        """
        # Import standard modules
        from json import dumps

        # Import third-party modules
        from pytest import raises
        from requests.exceptions import RequestException

        with raises(RequestException) as badRequest:
            binance.public.aggTrades(badSymbol)
            err = dumps(
                {
                    "url": (
                        "https://testnet.binance.vision/api/v3/"
                        f"aggTrades?symbol={badSymbol.upper()}"
                        "&limit=500"
                    ),
                    "status_code": 400,
                    "reason": "Bad Request",
                    "message": '{"code":-1121,"msg":"Invalid symbol."}'
                }
            )
            err in str(badRequest.value)

    def test_aggTrades_with_validDataTimeTimestampParameters(
        self, binance: Binance, aggTrades_keys: List[str], symbol: str,
        limit: int
    ):
        """Test with valid `startTime` and `endTime` (datetime) parameters."""
        # Import standard modules
        from datetime import datetime, timedelta

        startTime = datetime.now() - timedelta(days=1)
        endTime = startTime + timedelta(hours=1)
        aggTrades = binance.public.aggTrades(
            symbol, startTime, endTime, limit=limit
        )
        assert type(aggTrades) == list and (
            aggTrades == []
            or aggTrades_keys == sorted(next(iter(aggTrades)).keys())
        )

    def test_aggTrades_with_validStringTimestampParameters(
        self, binance: Binance, aggTrades_keys: List[str], symbol: str,
        limit: int
    ):
        """Test with valid `startTime` and `endTime` (str) parameters."""
        # Import standard modules
        from datetime import datetime, timedelta

        startTime = datetime.now() - timedelta(days=1)
        endTime = startTime + timedelta(hours=1)
        _startTime = str(startTime)
        _endTime = str(endTime)
        aggTrades = binance.public.aggTrades(
            symbol, _startTime, _endTime, limit=limit
        )
        assert type(aggTrades) == list and (
            aggTrades == []
            or aggTrades_keys == sorted(next(iter(aggTrades)).keys())
        )

    def test_aggTrades_with_invalidTimestampParameters(
        self, binance: Binance, symbol: str, limit: int
    ):
        """
        Test with invalid `startTime` and `endTime` parameters.

        Expect `RequestException` due to `endTime` - `startTime` > 1h.
        """
        # Import standard modules
        from datetime import datetime, timedelta
        from json import dumps

        # Import third-party modules
        from pytest import raises
        from requests.exceptions import RequestException

        startTime = datetime.now() - timedelta(days=1)
        endTime = startTime + timedelta(hours=2)

        with raises(RequestException) as badRequest:
            binance.public.aggTrades(symbol, startTime, endTime, limit=limit)
            err = dumps(
                {
                    "url": (
                        "https://testnet.binance.vision/api/v3/"
                        f"historicalTrades?symbol={symbol.upper()}"
                        f"&limit={limit}"
                        f"&startTime={datetime.timestamp(startTime)}"
                        f"&endTime={datetime.timestamp(endTime)}"
                    ),
                    "status_code": 400,
                    "reason": "Bad Request",
                    "message": (
                        '{"code":-1127,"msg":"More than 1 hours between '
                        'startTime and endTime."}'
                    )
                }
            )
            err in str(badRequest.value)

    def test_aggTrades_with_validFromIdParameter(
        self, binance: Binance, aggTrades_keys: List[str], symbol: str,
        limit: int
    ):
        """Test function with valid parameters."""
        aggTrades = binance.public.aggTrades(symbol, fromId=1, limit=limit)
        assert type(aggTrades) == list \
            and aggTrades_keys == sorted(next(iter(aggTrades)).keys())

    def test_aggTrades_with_invalidFromIdParameter(
        self, binance: Binance, symbol: str, limit: int
    ):
        """
        Test with invalid `fromId` parameter.

        Expect `RequestException`.
        """
        # Import standard modules
        from json import dumps

        # Import third-party modules
        from pytest import raises
        from requests.exceptions import RequestException

        with raises(RequestException) as badRequest:
            binance.public.aggTrades(symbol, fromId=-1, limit=10)
            err = dumps(
                {
                    "url": (
                        "https://testnet.binance.vision/api/v3/"
                        f"historicalTrades?symbol={symbol.upper()}"
                        f"&limit={limit}&fromId=-1"
                    ),
                    "status_code": 400,
                    "reason": "Bad Request",
                    "message": (
                        '{"code":-1100,"msg":"Illegal characters found in '
                        "parameter 'fromId'; legal range is '^[0-9]{1,20}"
                        '$\'."}'
                    )
                }
            )
            err in str(badRequest.value)


# TODO: Continue from here!


class TestBinanceKlines:
    """TODO: Add description."""

    def test_klines_with_noParameters(self, binance: Binance):
        """
        Test function without mandatory parameters.

        Expect `TypeError`.
        """
        # Import third-party modules
        from pytest import raises

        with raises(TypeError) as typeError:
            binance.public.klines()
            err = (
                "klines() missing 2 required positional arguments: "
                "'symbol' and 'interval'"
            )
            err in str(typeError.value)

    def test_klines_with_invalidSymbol(
        self, binance: Binance, badSymbol: str, interval: str
    ):
        """
        Test with invalid `symbol` and default optional parameters.

        Expect `RequestException`.
        """
        # Import standard modules
        from json import dumps

        # Import third-party modules
        from pytest import raises
        from requests.exceptions import RequestException

        with raises(RequestException) as badRequest:
            binance.public.klines(badSymbol, interval)
            err = dumps(
                {
                    "url": (
                        "https://testnet.binance.vision/api/v3/klines?"
                        f"symbol={badSymbol.upper()}&interval={interval}"
                        "&limit=500"
                    ),
                    "status_code": 400,
                    "reason": "Bad Request",
                    "message": '{"code":-1121,"msg":"Invalid symbol."}'
                }
            )
            err in str(badRequest.value)

    def test_klines_with_invalidInterval(self, binance: Binance, symbol: str):
        """
        Test with invalid `interval` and default optional parameters.

        Expect `RequestException`.
        """
        # Import standard modules
        from json import dumps

        # Import third-party modules
        from pytest import raises
        from requests.exceptions import RequestException

        with raises(RequestException) as badRequest:
            binance.public.klines(symbol, '1W')
            err = dumps(
                {
                    "url": (
                        "https://testnet.binance.vision/api/v3/klines?"
                        f"symbol={symbol.upper()}&interval=1W&limit=500"
                    ),
                    "status_code": 400,
                    "reason": "Bad Request",
                    "message": '{"code":-1121,"msg":"Invalid interval."}'
                }
            )
            err in str(badRequest.value)

    def test_klines_with_validParameters(
        self, binance: Binance, symbol: str, interval: str, limit: int
    ):
        """TODO: Add description."""
        klines = binance.public.klines(symbol, interval=interval, limit=limit)
        assert isinstance(klines, list) and len(next(iter(klines))) == 12


class TestBinanceAveragePrice:
    """TODO: Add description."""

    def test_avgPrice(self, binance: Binance, symbol: str):
        """TODO: Add description."""
        avgPrice = binance.public.avgPrice(symbol)
        expected_keys = ['mins', 'price']
        assert expected_keys == sorted(avgPrice.keys())


class TestBinancePriceTicker24:
    """TODO: Add description."""

    def test_priceTicker24(self, binance: Binance, symbol: str):
        """TODO: Add description."""
        priceTicker24 = binance.public.priceTicker24(symbol)
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

    def test_currentPrice(self, binance: Binance, symbol: str):
        """TODO: Add description."""
        currentPrice = binance.public.currentPrice(symbol)
        expected_keys = ['price', 'symbol']
        assert expected_keys == sorted(currentPrice.keys())


class TestBinanceBookTicker:
    """TODO: Add description."""

    def test_bookTicker(self, binance: Binance, symbol: str):
        """TODO: Add description."""
        bookTicker = binance.public.bookTicker(symbol)
        expected_keys = ['askPrice', 'askQty', 'bidPrice', 'bidQty', 'symbol']
        assert expected_keys == sorted(bookTicker.keys())
