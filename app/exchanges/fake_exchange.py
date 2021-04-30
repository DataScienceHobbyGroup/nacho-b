import logging

class fake_exchange:

    TRANSACTION_COST_FIXED = 0
    SECURITY = 'BTC'

    current_balance = 0
    profit_loss = 0

    num_purchases = 0
    num_sales = 0

    def buy(self, qty, value):
        amount_to_deduct = (qty * value) + self.TRANSACTION_COST_FIXED
        self.current_balance += qty
        self.profit_loss -= amount_to_deduct
        self.num_purchases += 1
        logging.info(f"I just bought {qty} {self.SECURITY} for {amount_to_deduct}")

    def sell(self, qty, value):
        amount_to_award = (qty * value) - self.TRANSACTION_COST_FIXED
        self.current_balance -= qty
        self.profit_loss += amount_to_award
        self.num_sales += 1
        logging.info(f"I just sold {qty} {self.SECURITY} for {amount_to_award}")

    def get_current_balance(self):
        '''The number of shares you own right now'''
        return self.current_balance

    def __init__(self,initial_investment):
        self.current_balance = initial_investment

    def trading_summary(self):
        emoji = "😂😂😂🤑🤑💰" if self.profit_loss > 0 else "😡😡😡🤬🤬🤬"
        return f'''
I made {self.num_purchases} purchases and {self.num_sales} sales and came away with a profit of {self.profit_loss} {emoji}
At the end of the game I am holding {self.current_balance} {self.SECURITY}'''

