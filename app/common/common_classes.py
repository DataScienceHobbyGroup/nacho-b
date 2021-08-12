"""
Author: Peter Ooms.

TODO: Add description.
"""


class transaction():
    """
    Transaction factory class.

    Produces a transaction based on buying or selling.
    """

    isBuyTransaction = False
    amount = 0
    desired_value = 0

    def buyTransactionFactory(amount, value):
        """Create a long transaction object."""
        new_trans = transaction()
        new_trans.isBuyTransaction = True
        new_trans.amount = amount
        new_trans.desired_value = value
        return new_trans

    def sellTransactionFactory(amount, value):
        """Create a short transaction object."""
        new_trans = transaction()
        new_trans.isBuyTransaction = False
        new_trans.amount = amount
        new_trans.desired_value = value
        return new_trans

    def __str__(self):
        """Produce string representation of this object."""
        if self.isBuyTransaction:
            return f"Request to buy {self.amount} " \
                f"security at {self.desired_value}"
        return f"Request to sell {self.amount} security at {self.desired_value}"
