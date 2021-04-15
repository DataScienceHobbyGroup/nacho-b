
def MA_strategy(source: str, ma_fast: int, ma_slow: int, open: bool = False, reverse: bool = False):
	import pandas as pd
	import matplotlib.pyplot as plt

	price_open_close = 'open' if open else 'close'
	_ma_fast = 'MA' + str(ma_fast)
	_ma_slow = 'MA' + str(ma_slow)

	# import coin pair data	
	coin_pair = pd.read_csv(source, index_col=0)
	# reverse data set. data should be ordered from oldest to newest
	if reverse:
		coin_pair = coin_pair.iloc[::-1]

	# add two columns - moving average 10 and moving average 50
	coin_pair[_ma_fast] = coin_pair[price_open_close].rolling(ma_fast).mean()
	coin_pair[_ma_slow] = coin_pair[price_open_close].rolling(ma_slow).mean()


	# Add a new column "shares", if MA10>MA50, denote as 1 (long one share of stock), otherwise, denote as 0 (do nothing)
	coin_pair['shares'] = [1 if coin_pair.loc[ei, _ma_fast]>coin_pair.loc[ei, _ma_slow] else 0 for ei in coin_pair.index]

	# add 2 new columns "close1" and "open1" which is the close or open price shifted back 1 so that the current periods close or open price and next periods close or open price are on the same record
	coin_pair['close1'] = coin_pair['close'].shift(-1)
	coin_pair['open1'] = coin_pair['open'].shift(-1)

	# Add a new column "Profit" using List Comprehension, for any rows in coin_pair, if shares=1, the profit is calculated as the close price of 
	# tomorrow - the close price of today. Otherwise the profit is 0.	
	coin_pair['profit'] = \
		[coin_pair.loc[ei, 'open1'] - coin_pair.loc[ei, 'open'] if coin_pair.loc[ei, 'shares']==1 else 0 for ei in coin_pair.index] if open \
			else [coin_pair.loc[ei, 'close1'] - coin_pair.loc[ei, 'close'] if coin_pair.loc[ei, 'shares']==1 else 0 for ei in coin_pair.index]
	
	# Plot a graph to show the Profit/Loss
	coin_pair['profit'].plot()
	plt.axhline(y=0, color='red')
	# plt.show()

	# Use .cumsum() to calculate the accumulated wealth over the period
	coin_pair['wealth'] = coin_pair['profit'].cumsum()

	# plot the wealth to show the growth of profit over the period
	coin_pair['wealth'].plot()
	plt.title('Total money you win is {}'.format(coin_pair.loc[coin_pair.index[-2], 'wealth']))
	plt.show()

# main
if __name__ == '__main__':
	MA_strategy('Binance_BTCUSDT_1h.csv', 10, 50, False, True)