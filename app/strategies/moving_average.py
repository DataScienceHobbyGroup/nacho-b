import logging
logger = logging.getLogger(__name__)

import curio
import pandas as pd
import numpy
import matplotlib.pyplot as plt
from collections import deque

from .base_class import strategy_base_class as strategy
from common.common_classes import transaction as t

class moving_average(strategy):

    data_source = []
    queue = []
    currently_holding = False

    async def buy(self, amount, value):
        await super().buy(amount,value)
        self.currently_holding = True

    async def sell(self, amount, value):
        await super().sell(amount,value)
        self.currently_holding = False

    async def run(self, ma_fast_window: int, ma_slow_window: int, open: bool = False):

        logger.info(f"Running the strategy. Parameters are: ma_fast = {ma_fast_window} ma_slow = {ma_slow_window} open = {open}")

        dataframe = self.data_source.data
        price_open_close = 'open' if open else 'close'

        moving_average_window = list()

        for data in self.data_source.get_next_row():
            
            moving_average_window.append(data[price_open_close])

            while len(moving_average_window) > ma_slow_window:
                moving_average_window.pop(0)

            if len(moving_average_window) == ma_slow_window:
                ma_fast = numpy.mean(moving_average_window[(-1 * ma_fast_window):])
                ma_slow = numpy.mean(moving_average_window)
                
                if ma_fast > ma_slow:
                    if not self.currently_holding:
                        logger.info(f"Asking the exchange to buy 1 security because ma_fast ({ma_fast}) is bigger than ma_slow ({ma_slow})")
                        await self.buy(1,data[price_open_close] )
            
                else:
                    if self.currently_holding:
                        logger.info(f"Asking the exchange to sell 1 security because ma_fast ({ma_fast}) is no longer bigger than ma_slow ({ma_slow}) and I have a position open")
                        await self.sell(1, data[price_open_close])

        return None