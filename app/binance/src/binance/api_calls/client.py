"""
Collection of `Spot Account/Trades` APIs.

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
    """Collection of `Spot Account/Trades` APIs."""

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
            `LIMIT_MAKER` are `LIMIT` orders that will be rejected, if they
            would immediately match and trade as a taker.
            `STOP_LOSS` and `TAKE_PROFIT` will execute a `MARKET` order when
            the `stopPrice` is reached.
            Any `LIMIT` or `LIMIT_MAKER` type order can be made an iceberg
            order by sending an `icebergQty`.
            Any order with an `icebergQty` MUST have `timeInForce` set to
            `GTC`.
            `MARKET` orders using the quantity field specifies the amount of
            the base asset the user wants to buy or sell at the market price.
            For example, sending a `MARKET` order on BTCUSDT will specify how
            much BTC the user is buying or selling.
            `MARKET` orders using `quoteOrderQty` specifies the amount the
            user wants to spend (when buying) or receive (when selling) the
            quote asset; the correct quantity will be determined based on the
            market liquidity and `quoteOrderQty`.

            Using BTCUSDT as an example:
            On the BUY side, the order will buy as many BTC as `quoteOrderQty`
            USDT can.
            On the SELL side, the order will sell as much BTC needed to receive
            `quoteOrderQty` USDT.
            `MARKET` orders using `quoteOrderQty` will not break
            `LOT_SIZE` filter rules; the order will execute a quantity that
            will have the notional value as close as possible to
            `quoteOrderQty`.
            Same `newClientOrderId` can be accepted only when the previous
            one is filled, otherwise the order will be rejected.
            Trigger order price rules against market price for both `MARKET`
            and `LIMIT` versions:
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
                Requred, if `type` in [
                    `LIMIT`, `STOP_LOSS_LIMIT`, `TAKE_PROFIT_LIMIT`
                ].
                Defaults to `None`.

            quantity (Optional[float]):
                TODO: It appears to be mandatory, but the documentation says
                otherwise. Check it!
                Requred, if `type` in [
                    `LIMIT`, `MARKET`, `STOP_LOSS`, `STOP_LOSS_LIMIT`,
                    `TAKE_PROFIT`, `TAKE_PROFIT_LIMIT`, `LIMIT_MAKER`
                ].
                Defaults to `None`.

            quoteOrderQty (Optional[float]):
                TODO: Add description.
                Requred, if `type` == `MARKET`.
                Defaults to `None`.

            price (Optional[float]):
                TODO: Add description.
                Requred, if `type` in [
                    `LIMIT`, `STOP_LOSS_LIMIT`, `TAKE_PROFIT_LIMIT`,
                    `LIMIT_MAKER`
                ].
                Defaults to `None`.

            newClientOrderId (Optional[str]):
                A unique id among open orders. Automatically generated, if not
                sent.
                TODO: Understand what the poet was trying to say and rephrase
                it.

            stopPrice (Optional[float]):
                Required, if `type` in [
                    `STOP_LOSS`, `STOP_LOSS_LIMIT`, `TAKE_PROFIT`,
                    `TAKE_PROFIT_LIMIT`
                ]
                Defaults to `None`.

            icebergQty (Optional[float]):
                Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to
                create an iceberg order.
                Defaults to `None`.

            newOrderRespType (Optional[Literal['ACK', 'RESULT', 'FULL']]):
                Set the response JSON. ACK, RESULT, or FULL; MARKET and LIMIT
                order types default to FULL, all other orders default to ACK.

            recvWindow (int):
                Time window in milliseconds to execute the order.
                The value cannot be greater than `60000`.
                Defaults to `5000`.

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
            `LIMIT_MAKER` are `LIMIT` orders that will be rejected, if they
            would immediately match and trade as a taker.
            `STOP_LOSS` and `TAKE_PROFIT` will execute a `MARKET` order when
            the `stopPrice` is reached.
            Any `LIMIT` or `LIMIT_MAKER` type order can be made an iceberg
            order by sending an `icebergQty`.
            Any order with an `icebergQty` MUST have `timeInForce` set to
            `GTC`.
            `MARKET` orders using the quantity field specifies the amount of
            the base asset the user wants to buy or sell at the market price.
            For example, sending a `MARKET` order on BTCUSDT will specify how
            much BTC the user is buying or selling.
            `MARKET` orders using `quoteOrderQty` specifies the amount the
            user wants to spend (when buying) or receive (when selling) the
            quote asset; the correct quantity will be determined based on the
            market liquidity and `quoteOrderQty`.

            Using BTCUSDT as an example:
            On the BUY side, the order will buy as many BTC as `quoteOrderQty`
            USDT can.
            On the SELL side, the order will sell as much BTC needed to receive
            `quoteOrderQty` USDT.
            `MARKET` orders using `quoteOrderQty` will not break
            `LOT_SIZE` filter rules; the order will execute a quantity that
            will have the notional value as close as possible to
            `quoteOrderQty`.
            Same `newClientOrderId` can be accepted only when the previous
            one is filled, otherwise the order will be rejected.
            Trigger order price rules against market price for both `MARKET`
            and `LIMIT` versions:
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
                Requred, if `type` in [
                    `LIMIT`, `STOP_LOSS_LIMIT`, `TAKE_PROFIT_LIMIT`
                ].
                Defaults to `None`.

            quantity (Optional[float]):
                TODO: It appears to be mandatory, but the documentation says
                otherwise. Check it!
                Requred, if `type` in [
                    `LIMIT`, `MARKET`, `STOP_LOSS`, `STOP_LOSS_LIMIT`,
                    `TAKE_PROFIT`, `TAKE_PROFIT_LIMIT`, `LIMIT_MAKER`
                ].
                Defaults to `None`.

            quoteOrderQty (Optional[float]):
                TODO: Add description.
                Requred, if `type` == `MARKET`.
                Defaults to `None`.

            price (Optional[float]):
                TODO: Add description.
                Requred, if `type` in [
                    `LIMIT`, `STOP_LOSS_LIMIT`, `TAKE_PROFIT_LIMIT`,
                    `LIMIT_MAKER`
                ].
                Defaults to `None`.

            newClientOrderId (Optional[str]):
                A unique id among open orders. Automatically generated, if not
                sent.
                TODO: Understand what the poet was trying to say and rephrase
                it.

            stopPrice (Optional[float]):
                Required, if `type` in [
                    `STOP_LOSS`, `STOP_LOSS_LIMIT`, `TAKE_PROFIT`,
                    `TAKE_PROFIT_LIMIT`
                ]
                Defaults to `None`.

            icebergQty (Optional[float]):
                Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to
                create an iceberg order.
                Defaults to `None`.

            newOrderRespType (Optional[Literal['ACK', 'RESULT', 'FULL']]):
                Set the response JSON. ACK, RESULT, or FULL; MARKET and LIMIT
                order types default to FULL, all other orders default to ACK.

            recvWindow (int):
                Time window in milliseconds to execute the order.
                The value cannot be greater than `60000`.
                Defaults to `5000`.

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
            `fromId` TradeId to fetch from. Default gets most recent trades.
            If `fromId` is set, it will get `id` >= the `fromId`.
            Otherwise most recent trades are returned.
            `limit` Default 500; max 1000.
            `recvWindow` value cannot be greater than `60000`.

        Parameters
        ----------
            symbol (str):
                Mandatory: Currency symbol of interest.
                Example: `BTCUSDT` for Bitcoin vs Tether
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
                now - `limit`
                Example: if `limit` is set to 10 the API will return
                the 10 previous trades.

            recvWindow (int):
                Time window in milliseconds to execute the order.
                The value cannot be greater than `60000`.
                Defaults to `5000`.

        Returns
        -------
            (List[dict])
            A list of all trades within a given range if set or the past X
            number of trades either specified or defaulted to `5000`.

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
            Either `orderId` or `origClientOrderId` must be sent.

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
                Defaults to `5000`.

        Returns
        -------
            (dict)
            Information regarding the cancelled order

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
                Defaults to `5000`.

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
            Either `orderId` or `origClientOrderId` must be sent.
            For some historical orders `cummulativeQuoteQty` will be < 0,
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
                Defaults to `5000`.

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
            If the `symbol` is not sent, orders for all symbols
            will be returned in an array.

        Parameters
        ----------
            symbol (str):
                Currency symbol.

            recvWindow (int):
                Number of milliseconds in which to complete the transaction.
                If timeout, transaction is being cancelled.
                Defaults to `5000`.

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


del(Literal, Optional, date, datetime)
