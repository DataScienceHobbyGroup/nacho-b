"""
Collection of ``Spot Account/Trades`` APIs.

Date: 2021-05-25
Author: Vitali Lupusor
"""

# Import standard modules
from datetime import date, datetime
from typing import Literal, Optional, Union

# Import local modules
from ..helpers import get, post, delete  # type: ignore
from ..helpers.type_literals import ResponseTypeOptions, TypeOptions  # type: ignore  # noqa: E501


class Trade:
    """Collection of ``Spot Account/Trades`` APIs."""

    def __init__(
        self, key: str, secret: str, url: Optional[str] = None
    ) -> None:
        """
        Initialise the class.

        Parameters
        ----------
            key (str):
                Binance API key.

            secret (str):
                TODO: Add description.

            url (Optional[str]):
                Server URL.
        """
        self.__key = key
        self.__secret = secret
        self._url = url

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
            ``STOP_LOSS`` and ``TAKE_PROFIT`` will execute a ``MARKET`` order
            when the ``stopPrice`` is reached.
            Any ``LIMIT`` or ``LIMIT_MAKER`` type order can be made an iceberg
            order by sending an ``icebergQty``.
            Any order with an ``icebergQty`` MUST have ``timeInForce`` set to
            ``GTC``.
            ``MARKET`` orders using the quantity field specifies the amount of
            the base asset the user wants to buy or sell at the market price.
            For example, sending a ``MARKET`` order on BTCUSDT will specify how
            much BTC the user is buying or selling.
            ``MARKET`` orders using ``quoteOrderQty`` specifies the amount the
            user wants to spend (when buying) or receive (when selling) the
            quote asset; the correct quantity will be determined based on the
            market liquidity and ``quoteOrderQty``.

            Using BTCUSDT as an example:
            On the BUY side, the order will buy as many BTC as
            ``quoteOrderQty`` USDT can.
            On the SELL side, the order will sell as much BTC needed to receive
            ``quoteOrderQty`` USDT.
            ``MARKET`` orders using ``quoteOrderQty`` will not break
            ``LOT_SIZE`` filter rules; the order will execute a quantity that
            will have the notional value as close as possible to
            ``quoteOrderQty``.
            Same ``newClientOrderId`` can be accepted only when the previous
            one is filled, otherwise the order will be rejected.
            Trigger order price rules against market price for both ``MARKET``
            and ``LIMIT`` versions:
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
            self._url, 'order', self.__key, self.__secret,
            symbol=symbol.upper(), side=side.upper(), type=type.upper(),
            timeInForce=_timeInForce, quantity=quantity,
            quoteOrderQty=quoteOrderQty, newClientOrderId=newClientOrderId,
            price=price, stopPrice=stopPrice, icebergQty=icebergQty,
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
            ``STOP_LOSS`` and ``TAKE_PROFIT`` will execute a ``MARKET`` order
            when the ``stopPrice`` is reached.
            Any ``LIMIT`` or ``LIMIT_MAKER`` type order can be made an iceberg
            order by sending an ``icebergQty``.
            Any order with an ``icebergQty`` MUST have ``timeInForce`` set to
            ``GTC``.
            ``MARKET`` orders using the quantity field specifies the amount of
            the base asset the user wants to buy or sell at the market price.
            For example, sending a ``MARKET`` order on BTCUSDT will specify how
            much BTC the user is buying or selling.
            ``MARKET`` orders using ``quoteOrderQty`` specifies the amount the
            user wants to spend (when buying) or receive (when selling) the
            quote asset; the correct quantity will be determined based on the
            market liquidity and ``quoteOrderQty``.

            Using BTCUSDT as an example:
            On the BUY side, the order will buy as many BTC as
            ``quoteOrderQty`` USDT can.
            On the SELL side, the order will sell as much BTC needed to receive
            ``quoteOrderQty`` USDT.
            ``MARKET`` orders using ``quoteOrderQty`` will not break
            ``LOT_SIZE`` filter rules; the order will execute a quantity that
            will have the notional value as close as possible to
            ``quoteOrderQty``.
            Same ``newClientOrderId`` can be accepted only when the previous
            one is filled, otherwise the order will be rejected.
            Trigger order price rules against market price for both ``MARKET``
            and ``LIMIT`` versions:
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
            self._url, 'order/test', key=self.__key, secret=self.__secret,
            symbol=symbol.upper(), side=side.upper(), type=type.upper(),
            timeInForce=_timeInForce, quantity=quantity,
            quoteOrderQty=quoteOrderQty, newClientOrderId=newClientOrderId,
            price=price, stopPrice=stopPrice, icebergQty=icebergQty,
            newOrderRespType=newOrderRespType, recvWindow=recvWindow
        )

    def myTrades(
        self,
        symbol: str,
        startTime: Optional[Union[str, date, datetime]] = None,
        endTime: Optional[Union[str, date, datetime]] = None,
        fromId: Optional[float] = None,
        limit: Optional[int] = None,
        recvWindow: int = 5000
    ) -> dict:
        """
        Get trades for a specific account and symbol.

        Weight: 10
        Data Source: Database

        Other info
        ----------
        ``fromId`` TradeId to fetch from. Default gets most recent trades.
        If ``fromId`` is set, it will get ``id`` >= the ``fromId``.
        Otherwise most recent trades are returned.
        ``limit`` Default 500; max 1000.
        ``recvWindow`` The value cannot be greater than ``60000``

        Parameters
        ----------
            symbol (str):
                Mandatory: Currency symbol of interest.
                Example: ``BTCUSDT`` for Bitcoin vs Tether
                (US dollar stablecoin)

            startTime (Optional[Union[str, date, datetime]]):
                TODO: confirm if time is expressed in ms
                Optional: The point in history to get data from.

            endTime (Optional[Union[str, date, datetime]]):
                TODO: confirm if time is expressed in ms
                Optional: The point in history to get data to.

            fromId (Optional[int]):
                Optional: The trade id to in which to get data from.

            limit (Optional[int]):
                Optional: The number of trades to get starting from
                now - ``limit``
                Example: if ``limit`` is set to 10 the API will return
                the 10 previous trades.

            recvWindow (int):
                Time window in milliseconds to execute the order.
                The value cannot be greater than 60000.
                Defaults to 5000.

        Returns
        -------
            (List[dict]):
                A list of all trades within a given range if set or the past X
                number of trades either specified or defaulted to 5000:-
                [
                    {
                        'symbol': 'BTCUSDT',
                        'id': 675286,
                        'orderId': 2518667,
                        'orderListId': -1,
                        'price': '50000.00000000',
                        'qty': '0.00019700',
                        'quoteQty': '9.85000000',
                        'commission': '0.00000000',
                        'commissionAsset': 'USDT',
                        'time': 1621011870116,
                        'isBuyer': False,
                        'isMaker': True,
                        'isBestMatch': True
                    }
                ]
        """
        return get(
            self._url, 'myTrades', key=self.__key, secret=self.__secret,
            symbol=symbol.upper(), startTime=startTime, endTime=endTime,
            fromId=fromId, limit=limit, recvWindow=recvWindow
        )

    def cancelOrder(
        self,
        symbol: str,
        orderId: Optional[int] = None,
        origClientOrderId: Optional[str] = None,
        newClientOrderId: Optional[float] = None,
        recvWindow: int = 5000
    ) -> dict:
        """
        Cancel an active order.

        Weight: 1
        Data Source: Matching Engine

        Other info
        ----------
        Either ``orderId`` or ``origClientOrderId`` must be sent.

        Parameters
        ----------
            symbol (str):
                Currency symbol.

            orderId (int):
                Specified when cancelling a specific order. Corresponds with
                the open order to be cancelled.

            origClientOrderId (str):
                When the order is created a clientOrderId is generated if
                not specified. This is equivelant to origClientOrderId and
                can be used in this parameter

            newClientOrderId (str):
                Used to uniquely identify this cancel. Automatically generated
                by default.

            recvWindow (int):
                Number of milliseconds in which to complete the transaction.
                If timeout, transaction is being cancelled.
                Defaults to 5000.

        Returns
        -------
            (dict):
                Information regarding the cancelled order:-
                {
                    'symbol': 'BTCUSDT',
                    'origClientOrderId': 'ux4BADmI0BopccaWjvU0r9',
                    'orderId': 4740711,
                    'orderListId': -1,
                    'clientOrderId': 'GmC4kcQCc2t4PAV6wbbpT5',
                    'price': '30000.00000000',
                    'origQty': '0.01000000',
                    'executedQty': '0.00000000',
                    'cummulativeQuoteQty': '0.00000000',
                    'status': 'CANCELED',
                    'timeInForce': 'GTC',
                    'type': 'LIMIT',
                    'side': 'BUY'
                }
        """
        return delete(
            self._url, 'order',
            key=self.__key,
            secret=self.__secret,
            symbol=symbol.upper(),
            orderId=orderId,
            origClientOrderId=origClientOrderId,
            newClientOrderId=newClientOrderId,
            recvWindow=recvWindow
        )

    def cancelAllOpenOrders(
        self,
        symbol: str,
        recvWindow: int = 5000
    ) -> dict:
        """
        Cancel all active orders on a symbol.

        This includes OCO orders.

        Weight: 1
        Data Source: Matching Engine

        Other info
        ----------
            Given a symbol, all open orders related to it will cancel.

        Parameters
        ----------
            symbol (str):
                Currency symbol.

            recvWindow (int):
                Number of milliseconds in which to complete the transaction.
                If timeout, transaction is being cancelled.
                Defaults to 5000.

        Returns
        -------
            (List[dict])
            Information confirming the cancellation of each trade that was
            open and the details of each trade.

            [
                {
                    'symbol': 'BTCUSDT',
                    'origClientOrderId': '6uZQaihpXuvhgoICkKv6kI',
                    'orderId': 4723160,
                    'orderListId': -1,
                    'clientOrderId': 'RH5lwa40NhLe0ibLTz0ydv',
                    'price': '30000.00000000',
                    'origQty': '1.00000000',
                    'executedQty': '0.00000000',
                    'cummulativeQuoteQty': '0.00000000',
                    'status': 'CANCELED',
                    'timeInForce': 'GTC',
                    'type': 'LIMIT',
                    'side': 'BUY'
                }
            ]
        """
        return delete(
            self._url, 'openOrders',
            key=self.__key,
            secret=self.__secret,
            symbol=symbol.upper(),
            recvWindow=recvWindow
        )

    def queryOrder(
        self,
        symbol: str,
        orderId: Optional[int] = None,
        origClientOrderId: Optional[str] = None,
        recvWindow: int = 5000
    ) -> dict:
        """
        Check an order's status.

        Weight: 2
        Data Source: Database

        Other info
        ----------
            Either ``orderId`` or ``origClientOrderId`` must be sent.
            For some historical orders ``cummulativeQuoteQty`` will be < 0,
            meaning the data is not available at this time.

        Parameters
        ----------
            symbol (str):
                Currency symbol.

            orderId (int):
                Specified when cancelling a specific order. Corresponds with
                the open order to be cancelled.

            origClientOrderId (str):
                When the order is created a clientOrderId is generated if
                not specified. This is equivelant to origClientOrderId and
                can be used in this parameter

            recvWindow (int):
                Number of milliseconds in which to complete the transaction.
                If timeout, transaction is being cancelled.
                Defaults to 5000.

        Returns
        -------
            (dict)
            Information regarding the trade that was queried.

            {
                'symbol': 'BTCUSDT',
                'orderId': 4740711,
                'orderListId': -1,
                'clientOrderId': 'ux4BADmI0BopccaWjvU0r9',
                'price': '30000.00000000',
                'origQty': '0.01000000',
                'executedQty': '0.00000000',
                'cummulativeQuoteQty': '0.00000000',
                'status': 'NEW',
                'timeInForce': 'GTC',
                'type': 'LIMIT',
                'side': 'BUY',
                'stopPrice': '0.00000000',
                'icebergQty': '0.00000000',
                'time': 1622039616234,
                'updateTime': 1622039616234,
                'isWorking': True,
                'origQuoteOrderQty': '0.00000000'
            }
        """
        return get(
            self._url, 'order',
            key=self.__key,
            secret=self.__secret,
            symbol=symbol.upper(),
            orderId=orderId,
            origClientOrderId=origClientOrderId,
            recvWindow=recvWindow
        )

    def openOrders(
        self,
        symbol: Optional[str],
        recvWindow: int = 5000
    ) -> dict:
        """
        Get all open orders on a symbol.

        Careful when accessing this with no symbol.

        Weight: 3 for a single symbol; 40 when the symbol parameter is omitted
        Data Source: Database

        Other info
        ----------
            If the ``symbol`` is not sent, orders for all symbols
            will be returned in an array.

        Parameters
        ----------
            symbol (str):
                Currency symbol.

            recvWindow (int):
                Number of milliseconds in which to complete the transaction.
                If timeout, transaction is being cancelled.
                Defaults to 5000.

        Returns
        -------
            (List[dict])
            A list of all open orders for a given symbol or all open orders,
            if no symbol is specified (see cautionary note).

            [
                {
                    'symbol': 'BTCUSDT',
                    'orderId': 4759918,
                    'orderListId': -1,
                    'clientOrderId': 'iXfVYUhccMcTNnl01TvW3Q',
                    'price': '30000.00000000',
                    'origQty': '0.01000000',
                    'executedQty': '0.00000000',
                    'cummulativeQuoteQty': '0.00000000',
                    'status': 'NEW',
                    'timeInForce': 'GTC',
                    'type': 'LIMIT',
                    'side': 'BUY',
                    'stopPrice': '0.00000000',
                    'icebergQty': '0.00000000',
                    'time': 1622045634930,
                    'updateTime': 1622045634930,
                    'isWorking': True,
                    'origQuoteOrderQty': '0.00000000'
                }
            ]
        """
        return get(
            self._url, 'openOrders',
            key=self.__key,
            secret=self.__secret,
            symbol=symbol.upper() if symbol else None,
            recvWindow=recvWindow
        )

    def allOrders(
        self,
        symbol: str,
        orderId: Optional[int] = None,
        startTime: Optional[Union[str, date, datetime]] = None,
        endTime: Optional[Union[str, date, datetime]] = None,
        limit: Optional[int] = None,
        recvWindow: int = 5000
    ) -> dict:
        """
        Get all account orders; active, canceled, or filled.

        Weight: 10 with symbol
        Data Source: Database

        Other info
        ----------

        If ``orderId`` is set, it will get orders >= that ``orderId``.
        Otherwise most recent orders are returned.
        For some historical orders ``cummulativeQuoteQty`` will be < 0,
        meaning the data is not available at this time.
        If ``startTime`` and/or ``endTime`` provided, ``orderId`` is not
        required.

        Parameters
        ----------
            symbol (str):
                Currency symbol.

            orderId (int):
                Specified when cancelling a specific order. Corresponds with
                the open order to be cancelled.

            startTime (Optional[Union[str, date, datetime]]):
                TODO: confirm if time is expressed in ms
                Optional: The point in history to get data from.

            endTime (Optional[Union[str, date, datetime]]):
                TODO: confirm if time is expressed in ms
                Optional: The point in history to get data to.

            limit (Optional[int]):
                Optional: The number of trades to get starting from
                now - ``limit``
                Example: if ``limit`` is set to 10 the API will return
                the 10 previous trades.

            recvWindow (int):
                Number of milliseconds in which to complete the transaction.
                If timeout, transaction is being cancelled.
                Defaults to 5000.

        Returns
        -------
            (List[dict])
            A list of all orders for a given symbol.
            [
                {
                    'symbol': 'BTCUSDT',
                    'orderId': 4759918,
                    'orderListId': -1,
                    'clientOrderId': 'iXfVYUhccMcTNnl01TvW3Q',
                    'price': '30000.00000000',
                    'origQty': '0.01000000',
                    'executedQty': '0.00000000',
                    'cummulativeQuoteQty': '0.00000000',
                    'status': 'NEW',
                    'timeInForce': 'GTC',
                    'type': 'LIMIT',
                    'side': 'BUY',
                    'stopPrice': '0.00000000',
                    'icebergQty': '0.00000000',
                    'time': 1622045634930,
                    'updateTime': 1622045634930,
                    'isWorking': True,
                    'origQuoteOrderQty': '0.00000000'
                }
            ]
        """
        return get(
            self._url,
            'allOrders',
            key=self.__key,
            secret=self.__secret,
            symbol=symbol.upper(),
            orderId=orderId,
            startTime=startTime,
            endTime=endTime,
            limit=limit,
            recvWindow=recvWindow
        )

    def account(
        self,
        recvWindow: int = 5000
    ) -> dict:
        """
        Get current account information.

        Weight: 10
        Data Source: Memory => Database

        Other info
        ----------

        Parameters
        ----------
            recvWindow (int):
                Time window in milliseconds to execute the order.
                The value cannot be greater than 60000.
                Defaults to 5000.

        Returns
        -------
            (List[dict]):
                A list of all trades within a given range if set or the past X
                number of trades either specified or defaulted to 5000:-
                [
                    {
                        'symbol': 'BTCUSDT',
                        'id': 675286,
                        'orderId': 2518667,
                        'orderListId': -1,
                        'price': '50000.00000000',
                        'qty': '0.00019700',
                        'quoteQty': '9.85000000',
                        'commission': '0.00000000',
                        'commissionAsset': 'USDT',
                        'time': 1621011870116,
                        'isBuyer': False,
                        'isMaker': True,
                        'isBestMatch': True
                    }
                ]
        """
        return get(
            self._url,
            'account',
            key=self.__key,
            secret=self.__secret,
            recvWindow=recvWindow
        )

    def oco(
        self,
        symbol: str,
        side: Literal['BUY', 'SELL'],
        quantity: float,
        price: float,
        stopPrice: float,
        listClientOrderId: Optional[str] = None,
        limitClientOrderId: Optional[str] = None,
        limitIcebergQty: Optional[float] = None,
        stopClientOrderId: Optional[str] = None,
        stopLimitPrice: Optional[float] = None,
        stopIcebergQty: Optional[float] = None,
        stopLimitTimeInForce: Optional[Literal['GTC', 'FOK', 'IOC']] = None,
        newOrderRespType: Optional[ResponseTypeOptions] = None,
        recvWindow: int = 5000
    ) -> dict:
        """
        Send in a new OCO

        Weight: 1
        Data Source: Matching Engine

        Other info
        ----------
        Price Restrictions:
            SELL: Limit Price > Last Price > Stop Price
            BUY: Limit Price < Last Price < Stop Price

        Quantity Restrictions:
            Both legs must have the same quantity
            ICEBERG quantities however do not have to be the same.

        Order Rate Limit
            OCO counts as 2 orders against the order rate limit.

        Parameters
        ----------
            symbol (str):
                Currency symbol.

            side (Literal['BUY', 'SELL']):
                Whether the position is long/buy or short/sell

            quantity (float):
                The quantity of the asset to buy.

            price (float):
                The price of which to buy an asset at. Remember:-
                    SELL: Limit Price > Last Price > Stop Price
                    BUY: Limit Price < Last Price < Stop Price

            stopPrice (float):
                When the price falls to this level a market order is created to
                essentially close the position due to the trade going against
                the intended side.

            listClientOrderId (Optional[str]):
                A unique Id for the entire orderList

            limitClientOrderId (Optional[str]):
                A unique Id for the limit order

            limitIcebergQty (Optional[float]):
                The quantity of the asset to buy.

            stopClientOrderId (Optional[str]):
                A unique Id for the stop loss/stop loss limit leg.

            stopLimitPrice (Optional[float]):
                When the price falls to this level a limit order is created to
                essentially close the position at the specified price due to
                the trade going against the intended side. Usually used to
                avoid gapping past the stopPrice. If provided,
                ``stopLimitTimeInForce`` is required.

            stopIcebergQty (Optional[float]):
                Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to
                create an iceberg order.
                Defaults to ``None``.

            stopLimitTimeInForce (Optional[Literal['GTC', 'FOK', 'IOC']]):
                Must be passed when using ``stopPriceLimit``
                Valid values are:
                GTC 	Good Till Canceled
                    An order will be on the book unless the order is canceled.
                IOC 	Immediate Or Cancel
                    An order will try to fill the order as much as it can
                    before the order expires.
                FOK 	Fill or Kill
                    An order will expire if the full order cannot be filled
                    upon execution.

            newOrderRespType (Optional[ResponseTypeOptions]):
                Set the response JSON. ACK, RESULT, or FULL; MARKET and LIMIT
                order types default to FULL, all other orders default to ACK.

            recvWindow (int):
                Time window in milliseconds to execute the order.
                The value cannot be greater than 60000.
                Defaults to 5000.

        Returns
        -------
            (Dict[str, List[dict]]):
                Information related to the overall OCO order, a list of orders
                and a report detailing the orders:-
                {
                    'orderListId': 4922,
                    'contingencyType': 'OCO',
                    'listStatusType': 'EXEC_STARTED',
                    'listOrderStatus': 'EXECUTING',
                    'listClientOrderId': 'PLNwO0VkIhqTaOyTbjzMJt',
                    'transactionTime': 1622390178451,
                    'symbol': 'BTCUSDT',
                    'orders':
                    [
                        {
                            'symbol': 'BTCUSDT',
                            'orderId': 5730856,
                            'clientOrderId': 'aRVtxZ0ytCpU5vbRSagtS1'
                        },
                        {
                            'symbol': 'BTCUSDT',
                            'orderId': 5730857,
                            'clientOrderId': 'cNhPm3TRaLEmqTrAHXq1wL'
                        }
                    ],
                    'orderReports':
                    [
                        {
                            'symbol': 'BTCUSDT',
                            'orderId': 5730856,
                            'orderListId': 4922,
                            'clientOrderId': 'aRVtxZ0ytCpU5vbRSagtS1',
                            'transactTime': 1622390178451,
                            'price': '51000.00000000',
                            'origQty': '0.01000000',
                            'executedQty': '0.00000000',
                            'cummulativeQuoteQty': '0.00000000',
                            'status': 'NEW',
                            'timeInForce': 'GTC',
                            'type': 'STOP_LOSS_LIMIT',
                            'side': 'BUY',
                            'stopPrice': '50000.00000000'
                        },
                        {
                            'symbol': 'BTCUSDT',
                            'orderId': 5730857,
                            'orderListId': 4922,
                            'clientOrderId': 'cNhPm3TRaLEmqTrAHXq1wL',
                            'transactTime': 1622390178451,
                            'price': '30000.00000000',
                            'origQty': '0.01000000',
                            'executedQty': '0.00000000',
                            'cummulativeQuoteQty': '0.00000000',
                            'status': 'NEW',
                            'timeInForce': 'GTC',
                            'type': 'LIMIT_MAKER',
                            'side': 'BUY'
                        }
                    ]
                }
        """
        return post(
            self._url,
            'order/oco',
            key=self.__key,
            secret=self.__secret,
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
            stopPrice=stopPrice,
            listClientOrderId=listClientOrderId,
            limitClientOrderId=limitClientOrderId,
            limitIcebergQty=limitIcebergQty,
            stopClientOrderId=stopClientOrderId,
            stopLimitPrice=stopLimitPrice,
            stopIcebergQty=stopIcebergQty,
            stopLimitTimeInForce=stopLimitTimeInForce,
            newOrderRespType=newOrderRespType,
            recvWindow=recvWindow
        )

    def cancelOrderList(
        self,
        symbol: str,
        orderListId: Optional[float] = None,
        listClientOrderId: Optional[str] = None,
        newClientOrderId: Optional[str] = None,
        recvWindow: int = 5000
    ) -> dict:
        """
        Cancel an entire Order List.

        Weight: 1
        Data Source: Matching Engine

        Other info
        ----------
            Canceling an individual leg will cancel the entire OCO.
            Either ``orderListId`` or ``listClientOrderId`` must be provided
            ``newClientOrderId`` is used to uniquely identify this cancel, 
            automatically generated by default

        Parameters
        ----------
            symbol (str):
                Currency symbol.

            orderListId (Optional[float]):
                Whether the position is long/buy or short/sell

            listClientOrderId (Optional[str]):
                A unique Id for the entire orderList

            newClientOrderId (float):
                Used to uniquely identify this cancel

            recvWindow (int):
                Time window in milliseconds to execute the order.
                The value cannot be greater than 60000.
                Defaults to 5000.

        Returns
        -------
            (Dict[str, List[dict]]):
                Information related to the cancellation of the overall OCO
                order, a list of orders and a report detailing the orders:-
                    {
                        'orderListId': 4923,
                        'contingencyType': 'OCO',
                        'listStatusType': 'ALL_DONE',
                        'listOrderStatus': 'ALL_DONE',
                        'listClientOrderId': '7S91ZYqjQzKnylUO8IABGb',
                        'transactionTime': 1622393508893,
                        'symbol': 'BTCUSDT',
                        'orders':
                        [
                            {
                                'symbol': 'BTCUSDT',
                                'orderId': 5739602,
                                'clientOrderId': 'gFoIpd2GxKb1RJMvN7dSUc'
                            },
                            {
                                'symbol': 'BTCUSDT',
                                'orderId': 5739603,
                                'clientOrderId': '8QzeCXJ1qFQdiDPiSczVRg'
                            }
                        ],
                        'orderReports':
                        [
                            {
                                'symbol': 'BTCUSDT',
                                'origClientOrderId': 'gFoIpd2GxKb1RJMvN7dSUc',
                                'orderId': 5739602,
                                'orderListId': 4923,
                                'clientOrderId': 'Ay5LlXYalziLSEswKSjWIM',
                                'price': '49000.00000000',
                                'origQty': '0.01000000',
                                'executedQty': '0.00000000',
                                'cummulativeQuoteQty': '0.00000000',
                                'status': 'CANCELED',
                                'timeInForce': 'GTC',
                                'type': 'STOP_LOSS_LIMIT',
                                'side': 'BUY',
                                'stopPrice': '50000.00000000'
                            },
                            {
                                'symbol': 'BTCUSDT',
                                'origClientOrderId': '8QzeCXJ1qFQdiDPiSczVRg',
                                'orderId': 5739603,
                                'orderListId': 4923,
                                'clientOrderId': 'Ay5LlXYalziLSEswKSjWIM',
                                'price': '30000.00000000',
                                'origQty': '0.01000000',
                                'executedQty': '0.00000000',
                                'cummulativeQuoteQty': '0.00000000',
                                'status': 'CANCELED',
                                'timeInForce': 'GTC',
                                'type': 'LIMIT_MAKER',
                                'side': 'BUY'
                            }
                        ]
                    }
        """
        return delete(
            self._url,
            'orderList',
            key=self.__key,
            secret=self.__secret,
            symbol=symbol,
            orderListId=orderListId,
            listClientOrderId=listClientOrderId,
            newClientOrderId=newClientOrderId,
            recvWindow=recvWindow
        )

    def allOrderList(
        self,
        fromId: Optional[str] = None,
        startTime: Optional[Union[str, date, datetime]] = None,
        endTime: Optional[Union[str, date, datetime]] = None,
        limit: Optional[int] = None,
        recvWindow: int = 5000
    ) -> dict:
        """
        Retrieves all OCO based on provided optional parameters.

        Weight: 10
        Data Source: Database

        Other info
        ----------

        If ``fromID`` supplied, neither ``startTime`` or ``endTime`` can be
        provided.

        Parameters
        ----------
            fromId (Optional[str]):
                The Id of the OCO to start from. Eg. fromId should be from
                and order older than now.

            startTime (Optional[Union[str, date, datetime]]):
                TODO: confirm if time is expressed in ms
                Optional: The point in history to get data from.

            endTime (Optional[Union[str, date, datetime]]):
                TODO: confirm if time is expressed in ms
                Optional: The point in history to get data to.

            limit (Optional[int]):
                Optional: The number of trades to get starting from
                now - ``limit``
                Example: if ``limit`` is set to 10 the API will return
                the 10 previous trades.

            recvWindow (int):
                Number of milliseconds in which to complete the transaction.
                If timeout, transaction is being cancelled.
                Defaults to 5000.

        Returns
        -------
            (List[dict]):
                A list of all oco orders for the given parameters.
                [
                    {
                        'orderListId': 4921,
                        'contingencyType': 'OCO',
                        'listStatusType': 'ALL_DONE',
                        'listOrderStatus': 'ALL_DONE',
                        'listClientOrderId': 'vngnEJ8Zdy8XF0lhwTgux3',
                        'transactionTime': 1622389489116,
                        'symbol': 'BTCUSDT',
                        'orders':
                        [
                            {
                                'symbol': 'BTCUSDT',
                                'orderId': 5729322,
                                'clientOrderId': 'J1Pe3pq2LAPCgPiffgDbSl'
                            },
                            {
                                'symbol': 'BTCUSDT',
                                'orderId': 5729323,
                                'clientOrderId': 'JCgR0zZitgIf5PYXucdS3h'
                            }
                        ]
                    },
                    {
                        'orderListId': 4922,
                        'contingencyType': 'OCO',
                        'listStatusType': 'ALL_DONE',
                        'listOrderStatus': 'ALL_DONE',
                        'listClientOrderId': 'PLNwO0VkIhqTaOyTbjzMJt',
                        'transactionTime': 1622390178451,
                        'symbol': 'BTCUSDT',
                        'orders':
                        [
                            {
                                'symbol': 'BTCUSDT',
                                'orderId': 5730856,
                                'clientOrderId': 'aRVtxZ0ytCpU5vbRSagtS1'
                            },
                            {
                                'symbol': 'BTCUSDT',
                                'orderId': 5730857,
                                'clientOrderId': 'cNhPm3TRaLEmqTrAHXq1wL'
                            }
                        ]
                    },
                    {'orderListId': 4923,
                        'contingencyType': 'OCO',
                        'listStatusType': 'ALL_DONE',
                        'listOrderStatus': 'ALL_DONE',
                        'listClientOrderId': '7S91ZYqjQzKnylUO8IABGb',
                        'transactionTime': 1622393416854,
                        'symbol': 'BTCUSDT',
                        'orders':
                        [
                            {
                                'symbol': 'BTCUSDT',
                                'orderId': 5739602,
                                'clientOrderId': 'gFoIpd2GxKb1RJMvN7dSUc'
                            },
                            {
                                'symbol': 'BTCUSDT',
                                'orderId': 5739603,
                                'clientOrderId': '8QzeCXJ1qFQdiDPiSczVRg'
                            }
                        ]
                    }
                ]
        """
        return get(
            self._url,
            'allOrderList',
            key=self.__key,
            secret=self.__secret,
            fromId=fromId,
            startTime=startTime,
            endTime=endTime,
            limit=limit,
            recvWindow=recvWindow
        )


del(Literal, Optional, date, datetime)
