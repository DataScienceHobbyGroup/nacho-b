import pandas as pd
import matplotlib.pyplot as plt

class moving_average:

	data_source = []
	exchange = []

	def __init__(self, data_source, exchange):
		self.data_source = data_source
		self.exchange = exchange

	def run(self, ma_fast: int, ma_slow: int, open: bool = False):

		coin_pair = self.data_source.data
		exchange = self.exchange

		price_open_close = 'open' if open else 'close'
		_ma_fast = 'MA' + str(ma_fast)
		_ma_slow = 'MA' + str(ma_slow)
	
		# add two columns - moving average 10 and moving average 50
		coin_pair[_ma_fast] = coin_pair[price_open_close].rolling(ma_fast).mean()
		coin_pair[_ma_slow] = coin_pair[price_open_close].rolling(ma_slow).mean()
	
		for row in coin_pair.index:
			if coin_pair.loc[row, _ma_fast]>coin_pair.loc[row, _ma_slow]:
				if exchange.get_current_balance() < 1:
					exchange.buy(1,coin_pair.loc[row, price_open_close])
			
			else:
				if exchange.get_current_balance() > 0:
					exchange.sell(1, coin_pair.loc[row, price_open_close])

		return exchange