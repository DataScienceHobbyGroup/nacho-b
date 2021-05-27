"""
Test cases for Binance SDK.

IMPORTANT!
----------
    In order for it to work, ``binance`` package has to locally installed.
    I will draft the instruction on how to do it later.

    Don't try it at home without adult supervision!

Date: 2021-05-27
Author: Vitali Lupusor
"""

# Import local modules
from binance import Binance

dotenv = '.env'  # Relative path to ``.env`` file
binance = Binance.from_env_file(dotenv)


class TestBinanceMarket:
    """TODO: Add description."""

    def test_serverTime(self):
        """TODO: Add description."""
        # Import standard modules
        from datetime import datetime, timedelta

        serverTime = binance.public.serverTime()
        assert datetime.now() - serverTime < timedelta(seconds=2)

    def test_exchangeInfo(self):
        """TODO: Add description."""
        exchangeInfo = binance.public.exchangeInfo()
        expected_keys = [
            'exchangeFilters', 'rateLimits', 'serverTime', 'symbols',
            'timezone',
        ]
        assert expected_keys == sorted(exchangeInfo.keys())

    def test_orderBook(self):
        """TODO: Add description."""
        orderBook = binance.public.orderBook('bnbbtc')
        expected_keys = ['asks', 'bids', 'lastUpdateId']
        assert expected_keys == sorted(orderBook.keys())

    def test_recentTrades(self):
        """TODO: Add description."""
        recentTrades = binance.public.recentTrades('bnbbtc', 1)
        expected_keys = [
            'id', 'isBestMatch', 'isBuyerMaker', 'price', 'qty', 'quoteQty',
            'time',
        ]
        assert isinstance(recentTrades, list) \
            and expected_keys == sorted(next(iter(recentTrades)).keys())

    def test_tradeLookup(self):
        """TODO: Add description."""
        tradeLookup = binance.public.tradeLookup('bnbbtc', 1)
        expected_keys = [
            'id', 'isBestMatch', 'isBuyerMaker', 'price', 'qty', 'quoteQty',
            'time'
        ]
        assert isinstance(tradeLookup, list) \
            and expected_keys == sorted(next(iter(tradeLookup)).keys())

    def test_aggTrade(self):
        """TODO: Add description."""
        aggTrades = binance.public.aggTrades('bnbbtc', limit=1)
        expected_keys = ['M', 'T', 'a', 'f', 'l', 'm', 'p', 'q']
        assert type(aggTrades) == list \
            and expected_keys == sorted(next(iter(aggTrades)).keys())

    def test_klines(self):
        """TODO: Add description."""
        klines = binance.public.klines('bnbbtc', interval='1d', limit=1)
        assert isinstance(klines, list) and len(next(iter(klines))) == 12

    def test_avgPrice(self):
        """TODO: Add description."""
        avgPrice = binance.public.avgPrice('bnbbtc')
        expected_keys = ['mins', 'price']
        assert expected_keys == sorted(avgPrice.keys())

    def test_priceTicker24(self):
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

    def test_currentPrice(self):
        """TODO: Add description."""
        currentPrice = binance.public.currentPrice('bnbbtc')
        expected_keys = ['symbol', 'price']
        assert expected_keys == sorted(currentPrice.keys())

    def test_bookTicker(self):
        """TODO: Add description."""
        bookTicker = binance.public.bookTicker('bnbbtc')
        expected_keys = ['askPrice', 'askQty', 'bidPrice', 'bidQty', 'symbol']
        assert expected_keys == sorted(bookTicker.keys())


# class TestBinanceTrade:
#     """TODO: Add description."""

#     def test_order(self):
#         """TODO: Add description."""
#         ...

#     def test_testOrder(self):
#         """TODO: Add description."""
#         ...

#     def test_myTrades(self):
#         """TODO: Add description."""
#         ...

#     def test_cancelOrder(self):
#         """TODO: Add description."""
#         ...

#     def test_cancelAllOpenOrders(self):
#         """TODO: Add description."""
#         ...

#     def test_queryOrder(self):
#         """TODO: Add description."""
#         ...

#     def test_openOrders(self):
#         """TODO: Add description."""
#         ...
