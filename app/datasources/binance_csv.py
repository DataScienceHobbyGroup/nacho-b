import logging
logger = logging.getLogger(__name__)

import pandas as pd

class binance_csv:
    '''
    This class opens and transforms data held in a CSV file
    (binance format) and turns them into our standard format
    '''

    #Whether or not to reverse the data
    REVERSE = True
    
    #Empty object to store the pandas dataframe
    data = []

    def __init__(self, path:str):
        ''' Initialise a Binance formatted CSV file
        arguments: path(str) - path to the CSV file.
        '''
        self.data = pd.read_csv(path)
        
        # reverse data set. data should be ordered from oldest to newest
        if self.REVERSE:
            self.data = self.data.iloc[::-1]

        reverse = "Data was reversed." if self.REVERSE else "Data was not reversed."
        logger.info(f"Read {self.data.shape} from {path} successfully. {reverse}")

        # convert all dates to dd/mm/yyyy hr:min (13/04/2021 00:00) format
        dates = self.data['date']
        print(dates.head)
        dates = pd.to_datetime(dates)
        print()
        # remove duplicate values