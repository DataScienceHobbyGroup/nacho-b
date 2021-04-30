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
        self.data = pd.read_csv(path, index_col=0)
	    
        # reverse data set. data should be ordered from oldest to newest
        if self.REVERSE:
    	    self.data = self.data.iloc[::-1]