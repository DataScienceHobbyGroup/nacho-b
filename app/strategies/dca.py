import logging
logger = logging.getLogger(__name__)


class dca:

    data_source = []
    exchange = []

    def __init__(self, data_source, exchange):
        self.data_source = data_source
        self.exchange = exchange
        logger.info("Initialised the strategy.")

    def run(self, interval, dollar_amount):

        #logger.info(f"Running the strategy. Parameters are: ma_fast = {ma_fast} ma_slow = {ma_slow} open = {open}")

        coin_pair = self.data_source.data
        exchange = self.exchange
    
        count = 0
        for row in coin_pair.iterrows():
            if count % interval == 0:
                cost_1_btc = row[1]['close']
                buy_qty = dollar_amount / cost_1_btc
                exchange.buy(buy_qty,row[1]['close'])
            count += 1
        
        exchange.sell(exchange.get_current_balance, coin_pair.iloc[-1]['close'])

        return exchange