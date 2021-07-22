import pandas as pd
import logging
from curio import Queue, sleep
logger = logging.getLogger(__name__)

from . import base_class

class binance_csv(base_class.datasource_base_class):
    '''
    This class opens and transforms data held in a CSV file
    (binance format) and turns them into our standard format
    '''

    #Whether or not to reverse the data
    REVERSE = True
    
    #Empty object to store the pandas dataframe
    data = []

    #Position of the cursor
    cursor_position = 0

    #Queue on which to dump data
    q = []

    def __init__(self, path:str, q:Queue):
        ''' Initialise a Binance formatted CSV file
        arguments: path(str) - path to the CSV file.
        '''
        self.data = pd.read_csv(path)
        
        # reverse data set. data should be ordered from oldest to newest
        if self.REVERSE:
            self.data = self.data.iloc[::-1]

        reverse = "Data was reversed." if self.REVERSE else "Data was not reversed."
        logger.info(f"Read {self.data.shape} from {path} successfully. {reverse}")
        self.q = q

    def new_data_available(self):
        return not(self.cursor_position >= len(self.data))

    async def run(self):
        while self.new_data_available():
            logger.debug("Adding to queue...")
            await self.q.put(self.data.iloc[self.cursor_position])
            self.cursor_position += 1
            await sleep(0) # 0-second sleep allows the task loop to switch to the next ready task which gives the exchange a chance to run.
