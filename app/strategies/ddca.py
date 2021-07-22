'''
This strategy assumes that over a period of time called "investment_period"
with an investment amount called "total_investment" which is evenly divided
across the investment_period called "investment_installments", the risk of
suffering from market volitility is reduced. Therefore the investor will
have a position equal to an average price over the investment period.
Additionally, there will be some leniency on the time at which an
investment_installment is executed on an exchange if there is a high
probability that the market price will reduce in an acceptable amount of time
called "execution_tollerence". This tollerence will be dynamic thus the
extra "d" on ddca.
'''
import logging
logger = logging.getLogger(__name__)

import configparser

import math

class ddca:

    investment_period = 0
    total_investment = 0
    investment_installments = []
    execution_tollerence = 0

    data_source = []
    exchange = []

    configParser = configparser.RawConfigParser()

    def __init__(self, exchange, data_source=None):
        if data_source is None:
            logger.info(f'''Couldn't initialise the ddca strategy,
            data_source was: {data_source}''')
            return {"error": '''Couldn't initialise the ddca strategy,
            data_source was: {data_source}'''}
        self.data_source = data_source
        self.exchange = exchange


    def run(self, record_file):
        data_source = self.data_source.data
        exchange = self.exchange
        self.load_state(record_file)
        logger.info(f'''Running the strategy. 
        Parameters are: investment period = {self.investment_period} 
        total investment = {self.total_investment} 
        installments remaining = {len(self.investment_installments)}''')
        print(f'''Running the strategy. 
        Parameters are: investment period = {self.investment_period} 
        total investment = {self.total_investment} 
        installments remaining = {len(self.investment_installments)}''')
        
        self.save_state(record_file)
        return exchange

    def load_state(self, record_file):
        configFilePath = record_file
        self.configParser.read(configFilePath)
        if self.configParser.get('meta_state', 'in_progress').lower() == 'true':
            self.investment_period = int(self.configParser.get('state', 'investment_period'))
            self.total_investment = int(self.configParser.get('state', 'total_investment'))
            self.investment_installments = self.configParser.get('state', 'investment_installments')
        else:
            self.investment_period = int(self.configParser.get('initial', 'investment_period'))
            self.total_investment = int(self.configParser.get('initial', 'total_investment'))
            if(self.total_investment % self.investment_period == 0):
                installments_value = self.total_investment / self.investment_period
                for index in range(self.investment_period):
                    self.investment_installments.append(installments_value)
            elif self.total_investment % self.investment_period != 0:
                installments_value = math.floor(self.total_investment / self.investment_period)
                remainder_value = self.total_investment % self.investment_period
                for index in range(self.investment_period):
                    self.investment_installments.append(installments_value)
                self.investment_installments.append(remainder_value)
                pass

    def save_state(self, record_file):
        self.configParser.set('meta_state', 'in_progress', 'True')
        self.configParser.set('state', 'investment_period', self.investment_period)
        self.configParser.set('state', 'total_investment', self.total_investment)
        self.configParser.set('state', 'investment_installments', self.investment_installments)
        with open(record_file, 'w') as file:
            self.configParser.write(file)
        pass
