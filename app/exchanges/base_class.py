"""TODO: Add file description."""


from typing import List
from abc import ABCMeta, abstractmethod


class ExchangeBaseClass(metaclass=ABCMeta):
    """TODO: Add class description."""

    def __init__(self, queue, initial_investment=0):
        """TODO: Add function description."""
        self.q = queue
        self.current_balance = initial_investment

    # Access the command queue
    q: List = []

    @abstractmethod
    async def buy(self, qty, value):
        """TODO: Add function description."""
        pass

    @abstractmethod
    async def sell(self, qty, value):
        """TODO: Add function description."""
        pass

    @abstractmethod
    async def run(self):
        """TODO: Add function description."""
        while True:
            item = await self.q.get()
            if item.isBuyTransaction:
                await self.buy(item.amount, item.desired_value)
            else:
                await self.sell(item.amount, item.desired_value)
            await self.q.task_done()
