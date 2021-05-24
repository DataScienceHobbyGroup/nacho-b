"""TODO: Add file description."""

# Import standard modules
import logging

# Import local modules
from . import base_class

logger = logging.getLogger(__name__)


class FakeExchange(base_class.ExchangeBaseClass):
    """A representitive exchange that behaves just like a real exchange would."""

    def __init__(self, queue, initial_investment=0):
        """TODO: Add function description."""
        super().__init__(queue, initial_investment)
        logger.info(
            "Opened an initial account with the fake exchange with an "
            f"investment of {initial_investment}"
        )

    # The cost in USD to make a transaction
    TRANSACTION_COST_FIXED = 0

    # The security we are trading
    SECURITY_1 = 'BTC'
    SECURITY_2 = 'USD'

    # The number of the security we hold at any one time
    # Positive number = a long position, negative number = short
    current_balance = 0

    # Amount of currency spent or gained since the start
    currency_held = 0

    # Keeping track of now many buys and sells we've done
    num_purchases = 0
    num_sales = 0

    async def buy(self, qty, value):
        """Buy a number of the security at its current value."""
        # Deduct from currency held
        amount_to_deduct = (qty * value) + self.TRANSACTION_COST_FIXED
        self.currency_held -= amount_to_deduct

        # Credit the amount to security balance
        self.current_balance += qty

        # Calculate current standing
        profit_loss = (self.current_balance * value) + self.currency_held

        self.num_purchases += 1
        logger.info(
            f"Exch: BUY  {qty}x{self.SECURITY_1} for {amount_to_deduct}. "
            f"Current balance: {self.SECURITY_2} {self.currency_held}, "
            f"{self.SECURITY_1} {self.current_balance} P/L: {profit_loss}"
        )

    async def sell(self, qty, value):
        """Sell a number of the security at its current value."""
        # Add to currnecy held
        amount_to_award = (qty * value) - self.TRANSACTION_COST_FIXED
        self.currency_held += amount_to_award

        # Subtract from security balance
        self.current_balance -= qty

        # Calculate current standing
        profit_loss = (self.current_balance * value) + self.currency_held

        self.num_sales += 1
        logger.info(
            f"Exch: SELL {qty}x{self.SECURITY_1} for {amount_to_award}. "
            f"Current balance: {self.SECURITY_2} {self.currency_held}, "
            f"{self.SECURITY_1} {self.current_balance} P/L: {profit_loss}"
        )

    def get_current_balance(self):
        """Get the number of securities you own right now."""
        return self.current_balance

    async def run(self):
        """TODO: Add function description."""
        await super().run()
        await logger.info(trading_summary())
