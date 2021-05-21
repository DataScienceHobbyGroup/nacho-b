import curio      # async library
import logging    # python standard logging library
import click      # command line interface creation kit (click)
import click_log  # connects the logger output to click output

from datasources.binance_csv import binance_csv
from strategies.moving_average import moving_average
from strategies.dca import dca
from exchanges.fake_exchange import fake_exchange

logging.basicConfig(
        format='{asctime} - {name}: {levelname} $ {msg}',
        style='{',
        level=logging.INFO,
        handlers=[
            logging.FileHandler("last_run.log", mode='w'),
            logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
click_log.basic_config(logger)

LOGO = '''
                     __                __                                 
   ____  ____ ______/ /_  ____        / /_  ____ _____  ____ _____  ____ _
  / __ \/ __ `/ ___/ __ \/ __ \______/ __ \/ __ `/ __ \/ __ `/ __ \/ __ `/
 / / / / /_/ / /__/ / / / /_/ /_____/ /_/ / /_/ / / / / /_/ / / / / /_/ / 
/_/ /_/\__,_/\___/_/ /_/\____/     /_.___/\__,_/_/ /_/\__,_/_/ /_/\__,_/  

'''

# These 3 dicts match the strings passed in to the command lines to the 
# program modules. There is probably a cleaner/better way of acheiving 
# this but this works for now.
strategy_dict = {
    "moving_average" : moving_average,
    "dca"            : dca
}

exchange_dict = {
    "fake_exchange" : fake_exchange
}

datasource_dict = {
    "binance_csv" : binance_csv
}

@click.command()
@click.option('--strategy', help='Which strategy to use', type=click.Choice(strategy_dict.keys(), case_sensitive=False))
@click.option('--strategy_params', help='The parameters for the strategy, as a comma-separated list')
@click.option('--exchange', help='Which exchange to use', type=click.Choice(exchange_dict.keys()))
@click.option('--datasource', help='Which data source class to use', type=click.Choice(datasource_dict.keys()))
@click.option('--datasource_path', help='The path to the datasource csv', 
        type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=False, readable=True, resolve_path=False, allow_dash=True, path_type=str))
@click_log.simple_verbosity_option(logger)
def backtest(strategy, strategy_params, exchange, datasource, datasource_path):
    try:
        strategy_object = strategy_dict[strategy]
        exchange_object = exchange_dict[exchange]
        datasrce_object = datasource_dict[datasource]
    except:
        click.echo("Argument error.")
    from backtest import backtest_runner as bt
    curio.run(bt.run,
        strategy_object,
        exchange_object,
        datasrce_object, 
        strategy_params, 
        datasource_path)

@click.command()
@click.option('--strategy', help='Which strategy to use')
@click.option('--strategy_params', help='The parameters for the strategy, as a comma-separated list')
@click.option('--exchange', help='Which exchange to use')
@click.option('--datasource', help='Which data source class to use')
def connect_to_api():
    logger.info("This is where in the future we will connect to a live api and run the strategy indefinitely.")

@click.command()
@click.option('--strategy', help='Which strategy to use')
@click.option('--datasource', help='Which data source class to use')
@click.option('--datasource_path', help='The path to the datasource csv (if applicable)')
def optimise():
    logger.info("This is where in the future we will run a training algorithm to optimise the params of the strategy")

# Register the CLI commands
@click.group()
def cli(): pass
cli.add_command(backtest)
cli.add_command(connect_to_api)
cli.add_command(optimise)

# Entrypoint
if __name__ == '__main__':
    logger.info(LOGO)
    cli()

