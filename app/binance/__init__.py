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
from datetime import date, datetime
from dotenv import load_dotenv
from typing import Any, Dict, List, Literal, Optional, Union

# Import local modules
from binance.helpers import get, post  # type: ignore

load_dotenv('.env')

OrderBookLimit = Literal[5, 10, 20, 50, 100, 500, 1000, 5000]
KlineInterval = Literal[
    '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d',
    '3d', '1w', '1M'
]
TypeOptions = Literal[
    'LIMIT', 'MARKET', 'STOP_LOSS', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT',
    'TAKE_PROFIT_LIMIT', 'LIMIT_MAKER'
]
ResponseTypeOptions = Literal['ACK', 'RESULT', 'FULL']


class Binance:
    """Binance APIs interaction object."""

    def __init__(
        self,
        key: Optional[str] = None,
        secret: Optional[str] = None,
        url: str = 'https://testnet.binance.vision/api/v3'
    ):
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
        """
        # Import standard modules
        from os import getenv

        self._key = key or getenv('API_KEY')
        self._secret = secret or getenv('API_SECRET')
        self._url = url

    @property
    def key(self):
        """Retrieve the API key."""
        return self._key

    @property
    def secret(self):
        """Retrieve the secret."""
        return self._secret

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

    def __repr__(self) -> str:
        """Configure object representation."""
        return f'<Binance: {self._url}>'

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

    def exchangeInfo(
        self, symbol: Optional[str] = None, symbols: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get current exchange trading rules and symbol information.

        Weight: 10
        Data Source: Memory

        Parameters
        ----------
            **params:
                symbol (Optional[str]):
                    Currency symbol.
                    Defaults to ``None``.

                symbols (Optional[List[str]]):
                    List of currency symbol.
                    Defaults to ``None``.

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
        _symbol = symbol.upper() if symbol else None
        _symbols = str(symbols).upper() \
            .replace(' ', '') \
            .replace('\'', '"') \
            if symbols else None

        return get(
            self._url, 'exchangeInfo', symbol=_symbol, symbols=_symbols
        )

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
                Defaults to ``100``.

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
                Takes values between ``1`` and ``1000``.
                Defaults to ``500``.

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

        Important
        ---------
        Currently not working.

        Parameters
        ----------
            symbol (str):
                Currency symbol.

            limit (int):
                TODO: Add description.
                Takes values between ``1`` and ``5000``.
                Defaults to ``500``.

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
            fromId=fromId, key=self._key
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

        If ``startTime`` and ``endTime`` are sent, time between ``startTime``
        and ``endTime`` must be less than 1 hour.
        If ``fromId``, ``startTime`` and ``endTime`` are not sent, the most
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
                Takes values between ``1`` and ``1000``.
                Defaults to ``500``.

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
        from .helpers import to_timestamp

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
        If ``startTime`` and ``endTime`` are not sent, the most recent klines
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
                Takes values between ``1`` and ``1000``.
                Defaults to ``500``.

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
        from .helpers import to_timestamp

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

        If the symbol is not sent, ``bookTickers`` for all symbols will be
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

    def order(
        self,
        symbol: str,
        side: Literal['BUY', 'SELL'],
        type: TypeOptions,
        timeInForce,  # : Optional[] = None,
        quantity: Optional[float] = None,
        quoteOrderQty: Optional[float] = None,
        price: Optional[float] = None,
        newClientOrderId: Optional[str] = None,
        stopPrice: Optional[float] = None,
        icebergQty: Optional[float] = None,
        newOrderRespType: Optional[ResponseTypeOptions] = None,
        recvWindow: int = 5000
    ) -> dict:
        """
        Place a new order.

        Weight: 1
        Data Source: Matching Engine

        Other info
        ----------
        ``LIMIT_MAKER`` are ``LIMIT`` orders that will be rejected, if they
        would immediately match and trade as a taker.
        ``STOP_LOSS`` and ``TAKE_PROFIT`` will execute a ``MARKET`` order when
        the ``stopPrice`` is reached.
        Any ``LIMIT`` or ``LIMIT_MAKER`` type order can be made an iceberg
        order by sending an ``icebergQty``.
        Any order with an ``icebergQty`` MUST have ``timeInForce`` set to
        ``GTC``.
        ``MARKET`` orders using the quantity field specifies the amount of the
        base asset the user wants to buy or sell at the market price.
        For example, sending a ``MARKET`` order on BTCUSDT will specify how
        much BTC the user is buying or selling.
        ``MARKET`` orders using ``quoteOrderQty`` specifies the amount the user
        wants to spend (when buying) or receive (when selling) the quote asset;
        the correct quantity will be determined based on the market liquidity
        and ``quoteOrderQty``.

        Using BTCUSDT as an example:
        On the BUY side, the order will buy as many BTC as ``quoteOrderQty``
        USDT can.
        On the SELL side, the order will sell as much BTC needed to receive
        ``quoteOrderQty`` USDT.
        ``MARKET`` orders using ``quoteOrderQty`` will not break ``LOT_SIZE``
        filter rules; the order will execute a quantity that will have the
        notional value as close as possible to ``quoteOrderQty``.
        Same ``newClientOrderId`` can be accepted only when the previous one is
        filled, otherwise the order will be rejected.
        Trigger order price rules against market price for both ``MARKET`` and
        ``LIMIT`` versions:
        Price above market price: STOP_LOSS -> BUY, TAKE_PROFIT -> SELL
        Price below market price: STOP_LOSS -> SELL, TAKE_PROFIT -> BUY

        Parameters
        ----------
            symbol (str):
                TODO: Add description.

            side (Literal['BUY', 'SELL']):
                TODO: Add description.

            type (TypeOptions):
                TODO: Add description.

            timeInForce (Optional[TODO]):
                TODO: Add description.
                Requred, if ``type`` in [
                    ``LIMIT``, ``STOP_LOSS_LIMIT``, ``TAKE_PROFIT_LIMIT``
                ].
                Defaults to ``None``.

            quantity (Optional[float]):
                TODO: It appears to be mandatory, but the documentation says
                otherwise. Check it!
                Requred, if ``type`` in [
                    ``LIMIT``, ``MARKET``, ``STOP_LOSS``, ``STOP_LOSS_LIMIT``,
                    ``TAKE_PROFIT``, ``TAKE_PROFIT_LIMIT``, ``LIMIT_MAKER``
                ].
                Defaults to ``None``.

            quoteOrderQty (Optional[float]):
                TODO: Add description.
                Requred, if ``type`` == ``MARKET``.
                Defaults to ``None``.

            price (Optional[float]):
                TODO: Add description.
                Requred, if ``type`` in [
                    ``LIMIT``, ``STOP_LOSS_LIMIT``, ``TAKE_PROFIT_LIMIT``,
                    ``LIMIT_MAKER``
                ].
                Defaults to ``None``.

            newClientOrderId (Optional[str]):
                A unique id among open orders. Automatically generated, if not
                sent.
                TODO: Understand what the poet was trying to say and rephrase
                it.

            stopPrice (Optional[float]):
                Required, if ``type`` in [
                    ``STOP_LOSS``, ``STOP_LOSS_LIMIT``, ``TAKE_PROFIT``,
                    ``TAKE_PROFIT_LIMIT``
                ]
                Defaults to ``None``.

            icebergQty (Optional[float]):
                Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to
                create an iceberg order.
                Defaults to ``None``.

            newOrderRespType (Optional[TODO]):
                Set the response JSON. ACK, RESULT, or FULL; MARKET and LIMIT
                order types default to FULL, all other orders default to ACK.

            recvWindow (int):
                Time window in milliseconds to execute the order.
                The value cannot be greater than 60000.
                Defaults to 5000.

        Returns
        -------
            (dict):
            TODO: Add description.
        """
        _timeInForce = timeInForce.upper() if timeInForce else None
        return post(
            self._url, 'order', self._key, self._secret, symbol=symbol.upper(),
            side=side.upper(), type=type.upper(), timeInForce=_timeInForce,
            quantity=quantity, quoteOrderQty=quoteOrderQty,
            newClientOrderId=newClientOrderId, price=price,
            stopPrice=stopPrice, icebergQty=icebergQty,
            newOrderRespType=newOrderRespType, recvWindow=recvWindow
        )

    def testOrder(
        self,
        symbol: str,
        side: Literal['BUY', 'SELL'],
        type: TypeOptions,
        timeInForce=None,  # : Optional[] = None,
        quantity: Optional[float] = None,
        quoteOrderQty: Optional[float] = None,
        price: Optional[float] = None,
        newClientOrderId: Optional[str] = None,
        stopPrice: Optional[float] = None,
        icebergQty: Optional[float] = None,
        newOrderRespType: Optional[ResponseTypeOptions] = None,
        recvWindow: int = 5000
    ) -> dict:
        """
        Place a new order.

        Weight: 1
        Data Source: Matching Engine

        Other info
        ----------
        ``LIMIT_MAKER`` are ``LIMIT`` orders that will be rejected, if they
        would immediately match and trade as a taker.
        ``STOP_LOSS`` and ``TAKE_PROFIT`` will execute a ``MARKET`` order when
        the ``stopPrice`` is reached.
        Any ``LIMIT`` or ``LIMIT_MAKER`` type order can be made an iceberg
        order by sending an ``icebergQty``.
        Any order with an ``icebergQty`` MUST have ``timeInForce`` set to
        ``GTC``.
        ``MARKET`` orders using the quantity field specifies the amount of the
        base asset the user wants to buy or sell at the market price.
        For example, sending a ``MARKET`` order on BTCUSDT will specify how
        much BTC the user is buying or selling.
        ``MARKET`` orders using ``quoteOrderQty`` specifies the amount the user
        wants to spend (when buying) or receive (when selling) the quote asset;
        the correct quantity will be determined based on the market liquidity
        and ``quoteOrderQty``.

        Using BTCUSDT as an example:
        On the BUY side, the order will buy as many BTC as ``quoteOrderQty``
        USDT can.
        On the SELL side, the order will sell as much BTC needed to receive
        ``quoteOrderQty`` USDT.
        ``MARKET`` orders using ``quoteOrderQty`` will not break ``LOT_SIZE``
        filter rules; the order will execute a quantity that will have the
        notional value as close as possible to ``quoteOrderQty``.
        Same ``newClientOrderId`` can be accepted only when the previous one is
        filled, otherwise the order will be rejected.
        Trigger order price rules against market price for both ``MARKET`` and
        ``LIMIT`` versions:
        Price above market price: STOP_LOSS -> BUY, TAKE_PROFIT -> SELL
        Price below market price: STOP_LOSS -> SELL, TAKE_PROFIT -> BUY

        Parameters
        ----------
            symbol (str):
                TODO: Add description.

            side (Literal['BUY', 'SELL']):
                TODO: Add description.

            type (TypeOptions):
                TODO: Add description.

            timeInForce (Optional[TODO]):
                TODO: Add description.
                Requred, if ``type`` in [
                    ``LIMIT``, ``STOP_LOSS_LIMIT``, ``TAKE_PROFIT_LIMIT``
                ].
                Defaults to ``None``.

            quantity (Optional[float]):
                TODO: It appears to be mandatory, but the documentation says
                otherwise. Check it!
                Requred, if ``type`` in [
                    ``LIMIT``, ``MARKET``, ``STOP_LOSS``, ``STOP_LOSS_LIMIT``,
                    ``TAKE_PROFIT``, ``TAKE_PROFIT_LIMIT``, ``LIMIT_MAKER``
                ].
                Defaults to ``None``.

            quoteOrderQty (Optional[float]):
                TODO: Add description.
                Requred, if ``type`` == ``MARKET``.
                Defaults to ``None``.

            price (Optional[float]):
                TODO: Add description.
                Requred, if ``type`` in [
                    ``LIMIT``, ``STOP_LOSS_LIMIT``, ``TAKE_PROFIT_LIMIT``,
                    ``LIMIT_MAKER``
                ].
                Defaults to ``None``.

            newClientOrderId (Optional[str]):
                A unique id among open orders. Automatically generated, if not
                sent.
                TODO: Understand what the poet was trying to say and rephrase
                it.

            stopPrice (Optional[float]):
                Required, if ``type`` in [
                    ``STOP_LOSS``, ``STOP_LOSS_LIMIT``, ``TAKE_PROFIT``,
                    ``TAKE_PROFIT_LIMIT``
                ]
                Defaults to ``None``.

            icebergQty (Optional[float]):
                Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to
                create an iceberg order.
                Defaults to ``None``.

            newOrderRespType (Optional[TODO]):
                Set the response JSON. ACK, RESULT, or FULL; MARKET and LIMIT
                order types default to FULL, all other orders default to ACK.

            recvWindow (int):
                Time window in milliseconds to execute the order.
                The value cannot be greater than 60000.
                Defaults to 5000.

        Returns
        -------
            (dict):
            TODO: Add description.
        """
        _timeInForce = timeInForce.upper() if timeInForce else None
        return post(
            self._url, 'order/test', key=self._key, secret=self._secret,
            symbol=symbol.upper(), side=side.upper(), type=type.upper(),
            timeInForce=_timeInForce, quantity=quantity,
            quoteOrderQty=quoteOrderQty, newClientOrderId=newClientOrderId,
            price=price, stopPrice=stopPrice, icebergQty=icebergQty,
            newOrderRespType=newOrderRespType, recvWindow=recvWindow
        )


del(Any, Dict, List, Literal, Optional, date)
