"""
Collection of Binance API calls wiht ``POST`` method.

Date: 2021-05-25
Author: Vitali Lupusor
"""

# Import standard modules
from typing import Literal, Optional

# Import local modules
from ..helpers import post  # type: ignore
from ..helpers.type_literals import ResponseTypeOptions, TypeOptions


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
            self._url, 'order/test', key=self.__key, secret=self.__secret,
            symbol=symbol.upper(), side=side.upper(), type=type.upper(),
            timeInForce=_timeInForce, quantity=quantity,
            quoteOrderQty=quoteOrderQty, newClientOrderId=newClientOrderId,
            price=price, stopPrice=stopPrice, icebergQty=icebergQty,
            newOrderRespType=newOrderRespType, recvWindow=recvWindow
        )


del(Literal, Optional)
