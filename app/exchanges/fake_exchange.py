import logging
logger = logging.getLogger(__name__)

from . import base_class

class fake_exchange(base_class.exchange_base_class):
    '''A representitive exchange that behaves just like a real exchange would.'''

    #The cost in USD to make a transaction
    TRANSACTION_COST_FIXED = 0

    #The security we are trading
    SECURITY_1 = 'BTC'
    SECURITY_2 = 'USD'

    #The number of the security we hold at any one time
    #Positive number = a long position, negative number = short
    current_balance = 0

    #Amount of currency spent or gained since the start
    currency_held = 0

    #Keeping track of now many buys and sells we've done
    num_purchases = 0
    num_sales = 0

    async def buy(self, qty, value):
        ''' Buy a number of the security at its current value '''
        
        #Deduct from currency held
        amount_to_deduct = (qty * value) + self.TRANSACTION_COST_FIXED
        self.currency_held -= amount_to_deduct

        #Credit the amount to security balance
        self.current_balance += qty

        #Calculate current standing
        profit_loss = (self.current_balance * value) + self.currency_held

        self.num_purchases += 1
        logger.info(f"Exch: Buying {qty}x{self.SECURITY_1} for {amount_to_deduct}. Current balance: {self.SECURITY_2} {self.currency_held}, {self.SECURITY_1} {self.current_balance} P/L: {profit_loss}")

    async def sell(self, qty, value):
        ''' Sell a number of the security at its current value '''

        #Add to currnecy held
        amount_to_award = (qty * value) - self.TRANSACTION_COST_FIXED
        self.currency_held += amount_to_award

        #Subtract from security balance
        self.current_balance -= qty

        #Calculate current standing
        profit_loss = (self.current_balance * value) + self.currency_held

        self.num_sales += 1
        logger.info(f"Exch: Buying {qty}x{self.SECURITY_1} for {amount_to_award}. Current balance: {self.SECURITY_2} {self.currency_held}, {self.SECURITY_1} {self.current_balance} P/L: {profit_loss}")

    def get_current_balance(self):
        '''The number of securities you own right now'''
        return self.current_balance

    def __init__(self,queue,initial_investment=0):
        super().__init__(queue,initial_investment)
        logger.info(f"Opened an initial account with the fake exchange with an investment of {initial_investment}")        

    async def run(self):
        await super().run()
        await logger.info( trading_summary())

    def trading_summary(self):
        emoji = "😂😂😂🤑🤑💰" if self.profit_loss > 0 else "😡😡😡🤬🤬🤬"
        return f'''
I made {self.num_purchases} purchases and {self.num_sales} sales and came away with a profit of {self.profit_loss} {emoji}
At the end of the game I am holding {self.current_balance} {self.SECURITY}'''

