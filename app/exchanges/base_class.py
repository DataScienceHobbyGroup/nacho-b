"""TODO: Add file description."""


class ExchangeBaseClass:
    """TODO: Add class description."""

    def __init__(self, queue, initial_investment=0):
        """TODO: Add class description."""
        self.q = queue
        self.current_balance = initial_investment

    # Access the command queue
    q = []

    async def buy(self, qty, value):
        """TODO: Add function description."""
        pass

    async def sell(self, qty, value):
        """TODO: Add class description."""
        pass

    async def run(self):
        """TODO: Add class description."""
        while True:
            item = await self.q.get()
            if item.isBuyTransaction:
                await self.buy(item.amount, item.desired_value)
            else:
                await self.sell(item.amount, item.desired_value)
            await self.q.task_done()
