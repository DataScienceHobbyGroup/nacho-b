import curio
import logging

from datasources.binance_csv import binance_csv
from strategies.moving_average import moving_average
from strategies.dca import dca
from exchanges.fake_exchange import fake_exchange

# Entrypoint
async def main():
    
    # Configure logging
    logging.basicConfig(
            format='{asctime} - {name}: {levelname} $ {msg}',
            style='{',
            level=logging.INFO,
            filename='last_run.log',
            filemode='w'
    )  
    
    #TODO: Create a backtest module which takes in parameters for strategy, queue, data and exchange to make this a one-liner.
    # tidy up this mess.

    # Backtest of moving average strategy
    transaction_queue = curio.Queue()
    ticker_queue = curio.Queue()
    data_source = binance_csv("data/Binance_BTCUSDT_1h.csv", ticker_queue)
    exchange = fake_exchange(transaction_queue)
    strategy_ma = moving_average(data_source, transaction_queue, ticker_queue)
    await strategy_ma.configure(10, 50)
    async with curio.TaskGroup() as g:
        await g.spawn(exchange.run)
        await g.spawn(strategy_ma.run)
        ds = await g.spawn(data_source.run)
        await ds.join()
        await g.cancel_remaining()
        async for task in g:
            logging.info(str(task) + 'completed.' + str(task.result))

    # Backtest of dollar-cost-average strategy
    transaction_queue = curio.Queue()
    ticker_queue = curio.Queue()
    data_source = binance_csv("data/Binance_BTCUSDT_1h.csv", ticker_queue)
    exchange = fake_exchange(transaction_queue)
    strategy_dca = dca(data_source, transaction_queue, ticker_queue)
    await strategy_dca.configure(10, 24)
    async with curio.TaskGroup() as g:
        await g.spawn(exchange.run)
        ds = await g.spawn(data_source.run)
        await g.spawn(strategy_dca.run)
        await ds.join()
        await g.cancel_remaining()
        async for task in g:
            logging.info(str(task) + 'completed.' + str(task.result))       

if __name__ == '__main__':
    curio.run(main, with_monitor=True)
