import curio
import logging
logger = logging.getLogger(__name__)

from datasources.base_class import datasource_base_class as ds
from common.common_classes import transaction as t

class strategy_base_class():
    
    queue = []

    def __init__(self, data_source:ds, queue:curio.Queue):
        self.data_source = data_source
        self.queue = queue
        logger.info(f"Initialised the {__name__} strategy.")

    async def buy(self, amount,value):
        await self.queue.put(t.buyTransactionFactory(amount, value))

    async def sell(self, amount, value):
        await self.queue.put(t.sellTransactionFactory(amount, value))