import logging
logger = logging.getLogger(__name__)

import pandas as pd
from .base_class import strategy_base_class as strategy

class dca(strategy):

    async def run(self, interval, dollar_amount):

        #TODO: log params.

    
        count = 0
        for row in self.data_source.get_next_row():
            if count % interval == 0:
                cost_1_btc = row['close']
                buy_qty = dollar_amount / cost_1_btc
                await super().buy(buy_qty,row['close'])
            count += 1
        
        #super().sell(exchange.get_current_balance(), coin_pair.iloc[-1]['close'])

        return None        #logger.info(f"Running the strategy. Parameters are: ma_fast = {ma_fast} ma_slow = {ma_slow} open = {open}")