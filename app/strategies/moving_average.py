import logging
logger = logging.getLogger(__name__)

import curio
import pandas as pd
import numpy
import matplotlib.pyplot as plt
from collections import deque
from datasources.base_class import datasource_base_class as ds

class moving_average:

    data_source = []
    queue = []
    amount_held = 0


    def __init__(self, data_source:ds, queue:curio.Queue):
        self.data_source = data_source
        self.queue = queue
        logger.info("Initialised the strategy.")

    async def buy(self, amount):
        await self.queue.put("BUY " + str(amount))
        self.amount_held += 1

    async def sell(self, amount):
        await self.queue.put("SELL " + str(amount))
        self.amount_held -= 1

    async def run(self, ma_fast_window: int, ma_slow_window: int, open: bool = False):

        logger.info(f"Running the strategy. Parameters are: ma_fast = {ma_fast_window} ma_slow = {ma_slow_window} open = {open}")

        dataframe = self.data_source.data
        price_open_close = 'open' if open else 'close'

        moving_average_window = list()

        print(self.queue)
        await self.queue.put("Test Message")

        for data in self.data_source.get_next_row():
            
            moving_average_window.append(data[price_open_close])

            while len(moving_average_window) > ma_slow_window:
                moving_average_window.pop(0)

            if len(moving_average_window) == ma_slow_window:
                ma_fast = numpy.mean(moving_average_window[(-1 * ma_fast_window):])
                ma_slow = numpy.mean(moving_average_window)
                
                if ma_fast > ma_slow:
                    if self.amount_held < 1:
                        logger.info(f"Asking the exchange to buy 1 security because ma_fast ({ma_fast}) is bigger than ma_slow ({ma_slow})")
                        await self.buy(1)
            
                else:
                    if self.amount_held > 0:
                        logger.info(f"Asking the exchange to sell 1 security because ma_fast ({ma_fast}) is no longer bigger than ma_slow ({ma_slow}) and I have a position open")
                        await self.sell(1)

        return None