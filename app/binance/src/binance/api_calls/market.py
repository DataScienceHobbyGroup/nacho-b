"""
Collection of `Market Data Endpoint` APIs.

Date: 2021-05-25
Author: Vitali Lupusor
"""

# Import standard modules
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

# Import local modules
from ..helpers import get  # type: ignore
from ..helpers.type_literals import KlineInterval, OrderBookLimit  # type: ignore # noqa: E501


class MarketData:
    """Collection of `Market Data Endpoint` APIs."""

    def __init__(
        self, key: Optional[str] = None, url: Optional[str] = None
    ) -> None:
        """
        Initialise the class.

        Parameters
        ----------
            key (Optional[str]):
                Binance API key.

            url (Optional[str]):
                Server URL.
        """
        self.__key = key
        self._url = url

    def serverTime(self) -> datetime:
        """
        Test connectivity to the Rest API and get the current server time.

        Weight: 1
        Data Source: Memory

        Returns
        -------
            (datetime.datetime)
            Current server time.
        """
        response = get(self._url, endpoint='time')

        return datetime.fromtimestamp(response['serverTime'] / 1000)

    def exchangeInfo(self, *symbols: str) -> Dict[str, Any]:
        """
        Get current exchange trading rules and symbol information.

        Weight: 10
        Data Source: Memory

        Parameters
        ----------
            *symbols (str):
                Currency symbols.

        Raises
        ------
            (requests.exceptions.RequestException)
                If any symbol provided in either symbol or symbols do not
                exist, the endpoint will throw an error.

        Returns
        -------
            (Dict[str, Any])
            TODO: Add description.
        """
        _symbols = str([symbol.upper() for symbol in symbols]) \
            .replace(' ', '') \
            .replace('\'', '"') \
            if symbols else None

        return get(self._url, 'exchangeInfo', symbols=_symbols)

    def orderBook(
        self, symbol: str, limit: OrderBookLimit = 100
    ) -> Dict[str, Any]:
        """
        Request the order registry.

        | Limit               | Weight |
        | :------------------ | -----: |
        | 5, 10, 20, 50, 100  | 1      |
        | 500                 | 5      |
        | 1000                | 10     |
        | 5000                | 50     |

        Data Source: Memory

        Parameters
        ----------
            symbol (str):
                Currency symbol.

            limit (Literal[5, 10, 20, 50, 100, 500, 1000, 5000]):
                The depth of the registry.
                Defaults to `100`.

        Returns
        -------
            (Dict[str, Any])
            A dictionary containing a list bids and one of offers.

            {
                "lastUpdateId": 1027024,
                "bids": [
                    [
                        "4.00000000",     // PRICE
                        "431.00000000"    // QTY
                    ]
                ],
                "asks": [
                    [
                        "4.00000200",
                        "12.00000000"
                    ]
                ]
            }
        """
        return get(self._url, 'depth', symbol=symbol.upper(), limit=limit)

    def recentTrades(
        self, symbol: str, limit: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Get recent trades.

        Weight: 1
        Data Source: Memory

        Parameters
        ----------
            symbol (str):
                Currency symbol.

            limit (int):
                TODO: Add description.
                Takes values between `1` and `1000`.
                Defaults to `500`.

        Returns
        -------
            (List[Dict[str, Any]])
            TODO: Add description.

            [
                {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "quoteQty": "48.000012",
                    "time": 1499865549590,
                    "isBuyerMaker": true,
                    "isBestMatch": true
                }
            ]
        """
        return get(self._url, 'trades', symbol=symbol.upper(), limit=limit)

    def tradeLookup(
        self,
        symbol: str,
        limit: int = 500,
        fromId: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get older market trades.

        Weight: 5
        Data Source: Database

        Parameters
        ----------
            symbol (str):
                Currency symbol.

            limit (int):
                TODO: Add description.
                Takes values between `1` and `5000`.
                Defaults to `500`.

            fromId (Optional[int]):
                TODO: Add description.

        Returns
        -------
            (List[Dict[str, Any]])
            TODO: Add description.

            [
                {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "quoteQty": "48.000012",
                    "time": 1499865549590,
                    "isBuyerMaker": true,
                    "isBestMatch": true
                }
            ]
        """
        return get(
            self._url, 'historicalTrades', symbol=symbol.upper(), limit=limit,
            fromId=fromId, key=self.__key
        )

    def aggTrades(
        self,
        symbol: str,
        startTime: Optional[Union[str, date, datetime]] = None,
        endTime: Optional[Union[str, date, datetime]] = None,
        fromId: Optional[int] = None,
        limit: int = 500,
    ) -> List[Dict[str, Any]]:
        """
        Get older market trades.

        Description
        -----------
            If `startTime` and `endTime` are sent, time between
            `startTime` and `endTime` must be less than 1 hour.
            If `fromId`, `startTime` and `endTime` are not sent, the most
            recent aggregate trades will be returned.

        Weight: 1
        Data Source: Database

        Parameters
        ----------
            symbol (str):
                Currency symbol.

            startTime (Optional[Union[str, datetime.date, datetime.datetime]]):
                Date/datetime object or thereof string representation to get
                aggregate trades from. INCLUSIVE.

            endTime (Optional[Union[str, datetime.date, datetime.datetime]]):
                Date/datetime object or thereof string representation to get
                aggregate trades until. INCLUSIVE.

            fromId (Optional[int]):
                ID get aggregate trades from INCLUSIVE.

            limit (int):
                TODO: Add description.
                Takes values between `1` and `1000`.
                Defaults to `500`.

        Returns
        -------
            (List[Dict[str, Any]])
            TODO: Add description.

            [
                {
                    "a": 26129,         // Aggregate tradeId
                    "p": "0.01633102",  // Price
                    "q": "4.70443515",  // Quantity
                    "f": 27781,         // First tradeId
                    "l": 27781,         // Last tradeId
                    "T": 1498793709153, // Timestamp
                    "m": true,          // Was the buyer the maker?
                    "M": true           // Was the trade the best price match?
                }
            ]
        """
        # Import local modules
        from ..helpers import to_timestamp  # type: ignore

        _startTime = to_timestamp(startTime) if startTime else None
        _endTime = to_timestamp(endTime) if endTime else None

        return get(
            self._url, 'aggTrades', symbol=symbol.upper(), limit=limit,
            fromId=fromId, startTime=_startTime, endTime=_endTime
        )

    def klines(
        self,
        symbol: str,
        interval: KlineInterval,
        startTime: Optional[Union[str, date, datetime]] = None,
        endTime: Optional[Union[str, date, datetime]] = None,
        limit: int = 500,
    ) -> List[List[Any]]:
        """
        Get kline/candlestick bars for a symbol.

        Klines are uniquely identified by their open time.
        If `startTime` and `endTime` are not sent, the most recent klines
        are returned.

        Weight: 1
        Data Source: Database

        Parameters
        ----------
            symbol (str):
                Currency symbol.

            interval (KlineInterval):
                Case sensitive!
                Valid options: [
                    '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h',
                    '8h', '12h', '1d', '3d', '1w', '1M'
                ].

            startTime (Optional[Union[str, datetime.date, datetime.datetime]]):
                Date/datetime object or thereof string representation to get
                aggregate trades from. INCLUSIVE.

            endTime (Optional[Union[str, datetime.date, datetime.datetime]]):
                Date/datetime object or thereof string representation to get
                aggregate trades until. INCLUSIVE.

            limit (int):
                TODO: Add description.
                Takes values between `1` and `1000`.
                Defaults to `500`.

        Returns
        -------
            (List[List[Any]])
            TODO: Add description.

            [
                [
                    1499040000000,      // Open time
                    "0.01634790",       // Open
                    "0.80000000",       // High
                    "0.01575800",       // Low
                    "0.01577100",       // Close
                    "148976.11427815",  // Volume
                    1499644799999,      // Close time
                    "2434.19055334",    // Quote asset volume
                    308,                // Number of trades
                    "1756.87402397",    // Taker buy base asset volume
                    "28.46694368",      // Taker buy quote asset volume
                    "17928899.62484339" // Ignore.
                ]
            ]
        """
        # Import local modules
        from ..helpers import to_timestamp  # type: ignore

        _startTime = to_timestamp(startTime) if startTime else None
        _endTime = to_timestamp(endTime) if endTime else None

        return get(
            self._url, 'klines', symbol=symbol.upper(), interval=interval,
            startTime=_startTime, endTime=_endTime, limit=limit
        )

    def avgPrice(self, symbol: str) -> Dict[str, Any]:
        """
        Get current average price for a symbol.

        Weight: 1
        Data Source: Memory

        Parameters
        ----------
            symbol (str):
                Currency symbol. Case insensiteve.

        Returns
        -------
            (Dict[str, Any])
            Dictionary with the time period window and its average price.

            {
                "mins": 5,
                "price": "9.35751834"
            }
        """
        return get(self._url, 'avgPrice', symbol=symbol.upper())

    def priceTicker24(
        self, symbol: Optional[str] = None
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Get 24 hour rolling window price change statistics.

        Careful when accessing this with no symbol. If the symbol is not sent,
        tickers for all symbols will be returned in an array.

        Weight: 1; 40 when the symbol parameter is omitted
        Data Source: Memory

        Parameters
        ----------
            symbol (Optional[str]):
                Currency symbol.

        Returns
        -------
            (Union[List[Dict[str, Any]], Dict[str, Any]])
            TODO: Add description.

            {
                "symbol": "BNBBTC",
                "priceChange": "-94.99999800",
                "priceChangePercent": "-95.960",
                "weightedAvgPrice": "0.29628482",
                "prevClosePrice": "0.10002000",
                "lastPrice": "4.00000200",
                "lastQty": "200.00000000",
                "bidPrice": "4.00000000",
                "askPrice": "4.00000200",
                "openPrice": "99.00000000",
                "highPrice": "100.00000000",
                "lowPrice": "0.10000000",
                "volume": "8913.30000000",
                "quoteVolume": "15.30000000",
                "openTime": 1499783499040,
                "closeTime": 1499869899040,
                "firstId": 28385,   // First tradeId
                "lastId": 28460,    // Last tradeId
                "count": 76         // Trade count
            }
        """
        symbol = symbol.upper() if symbol else None
        return get(self._url, 'ticker/24hr', symbol=symbol)

    def currentPrice(
        self, symbol: Optional[str] = None
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Get latest price for a symbol or symbols.

        If the symbol is not sent, tickers for all symbols will be returned in
        an array.

        Weight: 1; 2 when the symbol parameter is omitted
        Data Source: Memory

        Parameters
        ----------
            symbol (Optional[str]):
                Currency symbol.

        Returns
        -------
            (Union[List[Dict[str, Any]], Dict[str, Any]])
            List of dictionaries with the symbol of the currency and its
            price at the moment of request.

            {
                "symbol": "LTCBTC",
                "price": "4.00000200"
            }
        """
        symbol = symbol.upper() if symbol else None
        return get(self._url, 'ticker/price', symbol=symbol)

    def bookTicker(
        self, symbol: Optional[str] = None
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Get the best price/qty on the order book for a symbol or symbols.

        If the symbol is not sent, `bookTickers` for all symbols will be
        returned in an array.

        Weight: 1; 2 when the symbol parameter is omitted
        Data Source: Memory

        Parameters
        ----------
            symbol (Optional[str]):
                Currency symbol.

        Returns
        -------
            (Union[List[Dict[str, Any]], Dict[str, Any]])
            TODO: Add description.

            {
                "symbol": "LTCBTC",
                "bidPrice": "4.00000000",
                "bidQty": "431.00000000",
                "askPrice": "4.00000200",
                "askQty": "9.00000000"
            }
        """
        symbol = symbol.upper() if symbol else None
        return get(self._url, 'ticker/bookTicker', symbol=symbol)


del(Any, Dict, List, Optional, Union, date)
