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

    # Backtest of moving average strategy
    q = curio.Queue()
    data_source = binance_csv("data/Binance_BTCUSDT_1h.csv")
    exchange = fake_exchange(q)
    strategy_ma = moving_average(data_source, q)
    async with curio.TaskGroup() as g:
        await g.spawn(exchange.run)
        strat = await g.spawn(strategy_ma.run,10,50)
        await strat.join()
        await g.cancel_remaining()
        async for task in g:
            logging.info(str(task) + 'completed.' + str(task.result))

    # Backtest of dollar-cost-average strategy
    q = curio.Queue()
    data_source = binance_csv("data/Binance_BTCUSDT_1h.csv")
    exchange = fake_exchange(q)
    strategy_dca = dca(data_source, q)
    async with curio.TaskGroup() as g:
        await g.spawn(exchange.run)
        strat = await g.spawn(strategy_dca.run,10,50)
        await strat.join()
        await g.cancel_remaining()
        async for task in g:
            logging.info(str(task) + 'completed.' + str(task.result))       

    #exchg_task = await curio.spawn()
    #strat_task = await curio.spawn(strategy_ma.run(10,50))
    #await strat_task.join()
    #await exchg_task.cancel()    
    
    
    #output_ma = strategy_ma.run(10, 50, False)
    #logging.info(output_ma.trading_summary())

    #number = 24*30*4
    #output_dca = strategy_dca.run(number, number)
    #logging.info(output_dca.trading_summary())

if __name__ == '__main__':
    curio.run(main, with_monitor=True)
