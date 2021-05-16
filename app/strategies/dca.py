import logging
logger = logging.getLogger(__name__)

import pandas as pd
from .base_class import strategy_base_class as strategy

class dca(strategy):

    interval = 0
    dollar_amount = 0
    count = 0

    async def configure(self, interval, dollar_amount):
        self.interval = interval
        self.dollar_amount = dollar_amount
        logger.info(f"DCA strategy initialised with interval {interval} and dollar amount {dollar_amount}")

    async def process_tick(self, tick):
        if self.count % self.interval == 0:
            cost_1_btc = tick['close']
            buy_qty = self.dollar_amount / cost_1_btc
            await super().buy(buy_qty,tick['close'])
        self.count += 1
        return None