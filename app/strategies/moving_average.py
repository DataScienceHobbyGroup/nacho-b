import logging
logger = logging.getLogger(__name__)

import curio
import pandas as pd
import numpy
import matplotlib.pyplot as plt

from .base_class import strategy_base_class as strategy
from common.common_classes import transaction as t

class moving_average(strategy):

    currently_holding = False
    ma_fast_window = 0
    ma_slow_window = 0
    moving_average_window = list()
    price_open_close = 'close'

    async def buy(self, amount, value):
        await super().buy(amount,value)
        self.currently_holding = True

    async def sell(self, amount, value):
        await super().sell(amount,value)
        self.currently_holding = False

    async def configure(self, params:str):
        ParamsList = params.split(',')
        self.ma_fast_window = int(ParamsList[0])
        self.ma_slow_window = int(ParamsList[1])
        if len(ParamsList) > 2:
            self.price_open_close = bool(ParamsList[2])
        logger.info(f"Parameters are: ma_fast = {self.ma_fast_window} ma_slow = {self.ma_slow_window} open = {self.price_open_close}")

    async def process_tick(self, tick):
        self.moving_average_window.append(tick[self.price_open_close])

        while len(self.moving_average_window) > self.ma_slow_window:
            self.moving_average_window.pop(0)

        if len(self.moving_average_window) == self.ma_slow_window:
            ma_fast = numpy.mean(self.moving_average_window[(-1 * self.ma_fast_window):])
            ma_slow = numpy.mean(self.moving_average_window)
                
            if ma_fast > ma_slow:
                if not self.currently_holding:
                    logger.info(f"Asking the exchange to buy 1 security because ma_fast ({ma_fast}) is bigger than ma_slow ({ma_slow})")
                    await self.buy(1,tick[self.price_open_close] )
            
            else:
                if self.currently_holding:
                    logger.info(f"Asking the exchange to sell 1 security because ma_fast ({ma_fast}) is no longer bigger than ma_slow ({ma_slow}) and I have a position open")
                    await self.sell(1, tick[self.price_open_close])

        return None