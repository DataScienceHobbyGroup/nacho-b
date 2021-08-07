import requests as r
import pandas as pd
import logging
from curio import Queue, sleep

from datasources import base_class
logger = logging.getLogger(__name__)


class binance_api(base_class.DatasourceBaseClass):
    '''
    This class grabs data from the binance API
    and adds it to the queue for processing
    '''

    # Reversing the data isn't needed as it is already
    # in the right order
    REVERSE = False
    
    #Empty object to store the pandas dataframe
    data = []

    # Config fields
    SYMBOL = "BTCUSDT"
    INTERVAL = "5m"
    LIMIT = 500 # Default=500, max=1000

    #Position of the cursor
    cursor_position = 0

    #Queue on which to dump data
    q = []

    def __init__(self, path:str, q:Queue):
        ''' Connect to binance API and download the data'''
        
        #TODO: It would be good if the base URI could be configured on the CLI or via a config file instead of being hardcoded here.
        base_uri = f"https://testnet.binance.vision/api/v3/klines?symbol={self.SYMBOL}&interval={self.INTERVAL}&limit={self.LIMIT}"
        response = r.get(base_uri)
        if not response.status_code == 200:
            logger.critical(f"Error retrieving the binance data. {r.status_code}: {r.text}")
            raise ValueError("Not able to get binance data from API.")
        data = response.json()        
        column_headings = ['Open Date','Open','High','Low','close','Volume BTC','Close time','Volume USDT','tradecount','Taker buy base asset volume','Taker buy quote asset volume','Ignore']
        
        self.data = pd.DataFrame(data, columns=column_headings)
        self.data = self.data.apply(pd.to_numeric)

        # reverse data set if needed. data should be ordered from oldest to newest
        if self.REVERSE:
            self.data = self.data.iloc[::-1]

        reverse = "Data was reversed." if self.REVERSE else "Data was not reversed."
        logger.info(f"Read {self.data.shape} from {base_uri} successfully. {reverse}")
        self.q = q

    def new_data_available(self):
        return not(self.cursor_position >= len(self.data))

    async def run(self):
        while self.new_data_available():
            logger.debug("Adding to queue...")
            await self.q.put(self.data.iloc[self.cursor_position])
            self.cursor_position += 1
            await sleep(0) # 0-second sleep allows the task loop to switch to the next ready task which gives the exchange a chance to run.