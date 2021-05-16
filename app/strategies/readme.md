This folder contains alpha strategies.

They don't need to worry about data wrangling as this is handled inthe data source class.

Below is the general template for a strategy for it to work properly with the rest of the program:

```
from .base_class import strategy_base_class as strategy

class my_awesome_strategy(strategy):

    async def run(self, ma_fast_window: int, ma_slow_window: int, open: bool = False):

        for data in self.data_source.get_next_row():

            #Your logic goes here

            #To buy a security:
            await super().buy(amount,current_value)

            #To sell a security:
            await super().sell(amount,value)
```

This can then directly be called from main.py and will work automagically with the rest of the program.