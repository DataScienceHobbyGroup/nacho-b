class transaction():
    
    isBuyTransaction = False
    amount = 0
    desired_value = 0

    def buyTransactionFactory(amount, value):
        new_trans = transaction()
        new_trans.isBuyTransaction = True
        new_trans.amount = amount
        new_trans.desired_value = value
        return new_trans

    def sellTransactionFactory(amount, value):
        new_trans = transaction()
        new_trans.isBuyTransaction = False
        new_trans.amount = amount
        new_trans.desired_value = value
        return new_trans

    def __str__(self):
        if self.isBuyTransaction:
            return f"Request to buy {self.amount} security at {self.desired_value}"
        return f"Request to sell {self.amount} security at {self.desired_value}"