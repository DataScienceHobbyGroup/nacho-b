"""
TODO: Add description.

Author: Peter Ooms.
"""

from .base_class import StrategyBaseClass as strategy

import logging
logger = logging.getLogger(__name__)


class DCA(strategy):
    """TODO: Add description."""

    interval = 0
    dollar_amount = 0
    count = 0

    async def configure(self, params: str):
        ParamsList = params.split(',')
        self.interval = int(ParamsList[0])
        self.dollar_amount = int(ParamsList[1])
        logger.info(
            "DCA strategy initialised with interval "
            f"{self.interval} and dollar amount {self.dollar_amount}"
        )

    async def process_tick(self, tick):
        if self.count % self.interval == 0:
            cost_1_btc = tick['close']
            buy_qty = self.dollar_amount / cost_1_btc
            await super().buy(buy_qty, tick['close'])
        self.count += 1
        return None
