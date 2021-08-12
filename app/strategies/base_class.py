"""
Author: Petter Ooms.

TODO: Add description.
"""

from common.common_classes import transaction as t
from abc import ABCMeta, abstractmethod

import curio
import logging
logger = logging.getLogger(__name__)


class StrategyBaseClass(metaclass=ABCMeta):
    """TODO: Add description."""

    transaction_queue: curio.Queue = []
    ticker_queue: curio.Queue = []

    def __init__(self, transaction_queue: curio.Queue, ticker_queue: curio.Queue):
        """TODO: Add description."""
        self.transaction_queue = transaction_queue
        self.ticker_queue = ticker_queue
        logger.info(f"Initialised the {__name__} strategy.")

    async def buy(self, amount: float, value: float):
        """TODO: Add description."""
        await self.transaction_queue.put(t.buyTransactionFactory(amount, value))

    async def sell(self, amount: float, value):
        """TODO: Add description."""
        await self.transaction_queue.put(t.sellTransactionFactory(amount, value))

    @abstractmethod
    async def process_tick(self, data):
        """Process the logic of a strategy tick by tick."""
        logger.error(
            "If you are reading this you did not override the process_tick function properly."
        )

    async def run(self):
        """TODO: Add description."""
        while True:
            item = await self.ticker_queue.get()
            await self.process_tick(item)
            await self.ticker_queue.task_done()
