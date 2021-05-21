import curio
import logging
logger = logging.getLogger(__name__)

from datasources.base_class import datasource_base_class as ds
from common.common_classes import transaction as t

class strategy_base_class():
    
    transaction_queue = []
    ticker_queue = []

    def __init__(self, transaction_queue:curio.Queue, ticker_queue:curio.Queue):
        self.transaction_queue = transaction_queue
        self.ticker_queue = ticker_queue
        logger.info(f"Initialised the {__name__} strategy.")

    async def buy(self, amount,value):
        await self.transaction_queue.put(t.buyTransactionFactory(amount, value))

    async def sell(self, amount, value):
        await self.transaction_queue.put(t.sellTransactionFactory(amount, value))

    async def process_tick(self, data):
        logger.error("If you are reading this you did not override the process_tick function properly.")

    async def run(self):
        while True:
            item = await self.ticker_queue.get()
            await self.process_tick(item)
            await self.ticker_queue.task_done()