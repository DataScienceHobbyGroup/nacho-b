"""
Scraper for getting ticker data.

Date: 2021
Author: Barry Foye
"""

try:
    from app.datasources.scraper import scraper
except ImportError:
    import scraper as scraper
import yfinance as yf
import os
import os.path
import pandas as pd
try:
    from app.datasources.util import util as util
except ImportError:
    import util as util


class TickerScraper:
    """
    Collection of functions to gather financial data.

    TODO: Currently this class is written with a bias to Yahoo Finance
    and could be improved to handle scraping data from other sites.
    """

    YAHOO_FINANCE_TICKER_CLASS = 'Fw(600) C($linkColor)'
    TICKER_LIST_FILE = './data/ticker_list.csv'
    DEAD_TICKER_LIST_FILE = './data/dead_ticker_list.csv'

    def read_in_site_list(self, file=None):
        """Read in site list."""
        sites_urls = open(file)
        list_of_sites = sites_urls.read().split('\n')
        sites_urls.close()
        return list_of_sites

    def scrape_tickers(self, list_of_sites=None):
        """
        Scrape ticker symbols.

        TODO: Add logic to store any defunkt tickers
        """
        list_of_tickers = []
        for s in list_of_sites:
            list_of_tickers.extend(
                scraper.Scraper.scrape(s, self.YAHOO_FINANCE_TICKER_CLASS)
            )
        list_of_tickers = pd.Series(list_of_tickers)
        if list_of_tickers.duplicated().sum() > 0:
            print('duplicated')
        # When the list of tickers are returned we need to check first if the
        # ticker_list file already exists i.e. is this the first time the app
        # is being run?
        if not os.path.exists(self.TICKER_LIST_FILE):
            # If the file doesn't exist, create it and then save
            # the list to that file.
            self.save_data(list_of_tickers, self.TICKER_LIST_FILE)
        else:
            # Else if it does exist, read it, right join the new/fresh list
            # and then store it again by overwriting the file. This should
            # handle any new symbols and remove any defunkt symbols.
            old_ticker_list = pd.read_csv(
                self.TICKER_LIST_FILE,
                names=['ticks'],
                header=None,
                skiprows=[0]
            )
            # Left exclusive join for items in the old list, not in the new
            # list.
            dead_tickers = old_ticker_list.merge(
                list_of_tickers.to_frame(name='ticks'),
                how='left',
                indicator=True
            )
            dead_tickers = dead_tickers[dead_tickers['_merge'] == 'left_only']
            # keep the ticks column
            dead_tickers = dead_tickers['ticks']
            # Right join for items in the old list that exist in the new
            # list plus any new items.
            new_list = old_ticker_list.merge(
                list_of_tickers.to_frame(name='ticks'),
                how='right'
            )
            # Save the data.
            self.save_data(new_list, self.TICKER_LIST_FILE)
            self.save_data(
                dead_tickers,
                self.DEAD_TICKER_LIST_FILE,
                mode='a',
                header=False
            )

    def save_data(self, data=None, file=None, mode='w', header=True):
        """Save data to files."""
        data.to_csv(file, mode=mode, header=header)

    def download_yfinance_data(self):
        """Download data using the yfinance library and stores to csv."""
        ticker_list = pd.read_csv(
            self.TICKER_LIST_FILE,
            skiprows=[0],
            names=['ticks'],
            header=None
        )
        ticker_list = ticker_list['ticks'].squeeze()
        for idx, tick in ticker_list.items():
            a_ticker = yf.Ticker(tick)
            for interval in util.INTERVALS:
                interval_ = util.date_range(interval)
                file = f'./data/{tick}_data_{interval_["interval"]}.csv'
                if not os.path.exists(file):
                    if 'error' in interval_:
                        break
                    elif 'period' in interval_:
                        a_ticker.history(
                            period=interval_['period'],
                            interval=interval_['interval']
                            ).to_csv(
                                file,
                                mode='w'
                                )
                    elif 'start' in interval_ and 'end' in interval_:
                        a_ticker.history(
                            start=interval_['start'],
                            end=interval_['end'],
                            interval=interval_['interval']
                            ).to_csv(
                                file,
                                mode='w'
                                )
                    else:
                        print('Some bogus shit going on here')
                        break
                else:
                    if 'error' in interval_:
                        break
                    elif 'period' in interval_:
                        current_data = pd.read_csv(
                            file,
                            header=None
                        )
                        new_data = a_ticker.history(
                            period=interval_['period'],
                            interval=interval_['interval']
                            )
                            # .to_csv(
                            #     file,
                            #     mode='a'
                            #     )
                        current_data.merge
                    elif 'start' in interval_ and 'end' in interval_:
                        a_ticker.history(
                            start=interval_['start'],
                            end=interval_['end'],
                            interval=interval_['interval']
                            ).to_csv(
                                file,
                                mode='a'
                                )
                    else:
                        print('Some bogus shit going on here')
                        break
                util.rate_limiter()

    def validate_data(self, num_tickers: int = 0):
        """Validate the data - TODO."""
        if num_tickers == 0:
            return False
        # path joining version for other paths
        DIR = 'app/datasources/data'
        print(len([name for name in os.listdir(DIR) if os.path.isfile(
            os.path.join(DIR, name))])
            )


# Entrypoint
if __name__ == '__main__':
    ticker_scraper = TickerScraper()
    list_of_sites = ticker_scraper.read_in_site_list('resources/sites.txt')
    tickers = ticker_scraper.scrape_tickers(list_of_sites)
    # ticker_scraper.download_yfinance_data()
    # ticker_scraper.validate_data(len(tickers))
