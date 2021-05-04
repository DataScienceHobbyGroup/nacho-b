import logging

from datasources.binance_csv import binance_csv
from strategies.moving_average import moving_average
from strategies.dca import dca
from exchanges.fake_exchange import fake_exchange

# Entrypoint
if __name__ == '__main__':
    
    # Configure logging
    logging.basicConfig(
            format='{asctime} - {name}: {levelname} $ {msg}',
            style='{',
            level=logging.INFO,
            filename='last_run.log',
            filemode='w'
    )  
    
    # Import some data - the data_source class handles any wrangling we need to do
    data_source = binance_csv("data/Binance_BTCUSDT_1h.csv")

    # Pick an exchange (in this case a fake one but once we get going this class will be an
    # adapter class that calls out to the exchange's real API)
    exchange = fake_exchange(0)

    # Pick a strategy, and give it our exchange and data
    strategy_ma = moving_average(data_source, exchange)

    strategy_dca = dca(data_source, exchange)

    # Vamonos
    output_ma = strategy_ma.run(10, 50, False)
    logging.info(output_ma.trading_summary())

    number = 24*30*4
    output_dca = strategy_dca.run(number, number)
    logging.info(output_dca.trading_summary())



