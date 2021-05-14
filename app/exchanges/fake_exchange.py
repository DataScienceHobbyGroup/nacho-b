import logging
logger = logging.getLogger(__name__)

class fake_exchange:
    '''A representitive exchange that behaves just like a real exchange would.'''

    #The cost in USD to make a transaction
    TRANSACTION_COST_FIXED = 0

    #The security we are trading
    SECURITY = 'BTC'

    #The number of the security we hold at any one time
    #Positive number = a long position, negative number = short
    current_balance = 0

    #Running tracker of our profit or loss
    profit_loss = 0

    #Keeping track of now many buys and sells we've done
    num_purchases = 0
    num_sales = 0

    q = []

    async def buy(self, qty, value):
        ''' Buy a number of the security at its current value '''
        amount_to_deduct = (qty * value) + self.TRANSACTION_COST_FIXED
        self.current_balance += qty
        self.profit_loss -= amount_to_deduct
        self.num_purchases += 1
        logger.info(f"Exchange recieved and fulfilled a request to buy {qty} {self.SECURITY} for {amount_to_deduct}")

    async def sell(self, qty, value):
        ''' Sell a number of the security at its current value '''
        amount_to_award = (qty * value) - self.TRANSACTION_COST_FIXED
        self.current_balance -= qty
        self.profit_loss += amount_to_award
        self.num_sales += 1
        logger.info(f"Exchange recieved and fulfilled a request to sell {qty} {self.SECURITY} for {amount_to_award}")

    def get_current_balance(self):
        '''The number of securities you own right now'''
        return self.current_balance

    def __init__(self,queue,initial_investment=0):
        logger.info(f"Opened an initial account with the fake exchange with an investment of {initial_investment}")        
        self.q = queue
        self.current_balance = initial_investment

    async def run(self):
        print(self.q)
        while True:
            item = await self.q.get()
            print ('Got: ' + item)
            await self.q.task_done()

    def trading_summary(self):
        emoji = "😂😂😂🤑🤑💰" if self.profit_loss > 0 else "😡😡😡🤬🤬🤬"
        return f'''
I made {self.num_purchases} purchases and {self.num_sales} sales and came away with a profit of {self.profit_loss} {emoji}
At the end of the game I am holding {self.current_balance} {self.SECURITY}'''

