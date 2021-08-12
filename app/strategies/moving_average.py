"""
Simple moving average strategy based on crossover.

Author: Peter Ooms.
"""

# import curio
# import pandas as pd
from typing import List, Union
import numpy
# import matplotlib.pyplot as plt

from .base_class import StrategyBaseClass as strategy
# from common.common_classes import transaction as t
import logging
logger = logging.getLogger(__name__)


class moving_average(strategy):
    """Contains the logic for the sma strategy."""

    currently_holding = False
    ma_fast_window = 0
    ma_slow_window = 0
    moving_average_window: List = list()
    price_open_close: Union[str, bool] = 'close'

    async def buy(self, amount: float, value: float):
        await super().buy(amount, value)
        self.currently_holding = True

    async def sell(self, amount: float, value: float):
        await super().sell(amount, value)
        self.currently_holding = False

    async def configure(self, params: str):
        ParamsList = params.split(',')
        self.ma_fast_window = int(ParamsList[0])
        self.ma_slow_window = int(ParamsList[1])
        if len(ParamsList) > 2:
            self.price_open_close = bool(ParamsList[2])
        logger.info(f"Parameters are: ma_fast = {self.ma_fast_window} "
                    f"ma_slow = {self.ma_slow_window} open = {self.price_open_close}")

    async def process_tick(self, tick):
        self.moving_average_window.append(tick[self.price_open_close])

        while len(self.moving_average_window) > self.ma_slow_window:
            self.moving_average_window.pop(0)

        if len(self.moving_average_window) == self.ma_slow_window:
            ma_fast = numpy.mean(self.moving_average_window[(-1 * self.ma_fast_window):])
            ma_slow = numpy.mean(self.moving_average_window)

            if ma_fast > ma_slow:
                if not self.currently_holding:
                    logger.info(f"Asking the exchange to buy 1 security because ma_fast "
                                f"({ma_fast}) is bigger than ma_slow ({ma_slow})")
                    await self.buy(1, tick[self.price_open_close])

            else:
                if self.currently_holding:
                    logger.info(f"Asking the exchange to sell 1 security because ma_fast "
                                f"({ma_fast}) is no longer bigger than ma_slow ({ma_slow}) "
                                "and I have a position open")
                    await self.sell(1, tick[self.price_open_close])

        return None
