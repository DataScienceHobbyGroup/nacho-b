"""
Author: Peter Ooms.

TODO: Add description.
"""

# from datasources.base_class import DatasourceBaseClass as ds
from strategies.base_class import StrategyBaseClass as strat
from exchanges.base_class import ExchangeBaseClass as exch

import curio
import logging
logger = logging.getLogger(__name__)


class backtest_runner:
    """
    Backtest strategies.

    This class allows strategy backtesting.
    """

    async def run(
        strategy: strat,
        exchange: exch,
        datasource,
        strategy_params: str,
        datasource_path: str
    ):
        """TODO: Add description."""
        logger.info("Entering backtest routine.")

        # Get curio queues
        transaction_queue = curio.Queue()
        ticker_queue = curio.Queue()

        # Set up objects
        data_source_object = datasource(datasource_path, ticker_queue)
        exchange_object = exchange(transaction_queue)
        strategy_object = strategy(transaction_queue, ticker_queue)
        await strategy_object.configure(strategy_params)

        # Run the tasks
        async with curio.TaskGroup() as g:
            await g.spawn(exchange_object.run)
            await g.spawn(strategy_object.run)
            datasrce_task = await g.spawn(data_source_object.run)
            await datasrce_task.join()
            await g.cancel_remaining()
            async for task in g:
                logging.info(str(task) + 'completed.' + str(task.result))

        # Clean exit
        logger.info("Backtest complete, exiting cleanly.")
