"""
Scraper for getting ticker data.

Date: 2021
Author: Barry Foye
"""

from app.datasources.scraper import scraper
import yfinance as yf
import os
import os.path
# try:
from app.datasources.util import util as util
# except ImportError:
#     import util as util


class TickerScraper:
    """
    Collection of functions to gather financial data.

    TODO: Currently this class uis written with a bias to Yahoo Finance
    and could be improved to handle scraping data from other sites.
    """

    YAHOO_FINANCE_TICKER_CLASS = 'Fw(600) C($linkColor)'

    def read_in_site_list(self, file=None):
        """Read in site list."""
        sites_urls = open(file)
        list_of_sites = sites_urls.read().split('\n')
        sites_urls.close()
        return list_of_sites

    def scrape_tickers(self, list_of_sites=None):
        """Scrape ticker symbols."""
        list_of_tickers = []
        for s in list_of_sites:
            list_of_tickers.extend(
                scraper.scrape(s, self.YAHOO_FINANCE_TICKER_CLASS)
            )
        return list_of_tickers

# def get_ticker_data(self, list_of_tickers=None):
#     """Get scraped ticker data."""
#     ticker_data = []
#     for i in range(4):
#         ticker_data.append(yf.Ticker(list_of_tickers[i]))

# def save_ticker_data(self, data=None):
#     """Save data for later."""
#     for td in data:
#         print(td.info)
# TODO: for integration we need a way to store the scraped data
# in our DB.
# scrape tickers
# def scrape_tickers(self, list_of_sites=None):
#     list_of_tickers = []
#     for s in list_of_sites:
#         list_of_tickers.extend(scraper.scrape(
# s, self.YAHOO_FINANCE_TICKER_CLASS))
#     return list_of_tickers
# download yahoo finance data

    def download_yfinance_data(self, list_of_tickers=None):
        """Download data using the yfinance library and stores to csv."""
        for tick in list_of_tickers:
            a_ticker = yf.Ticker(tick)
            for interval in util.INTERVALS:
                interval_ = util.date_range(interval)
                if 'error' in interval_:
                    break
                elif 'period' in interval_:
                    a_ticker.history(
                        period=interval_['period'],
                        interval=interval_['interval']
                        ).to_csv(
                            f'./data/{tick}_data_{interval_["interval"]}.csv',
                            mode='w'
                            )
                elif 'start' in interval_ and 'end' in interval_:
                    a_ticker.history(
                        start=interval_['start'],
                        end=interval_['end'],
                        interval=interval_['interval']
                        ).to_csv(
                            f'./data/{tick}_data_{interval_["interval"]}.csv',
                            mode='w'
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
    # ticker_scraper.download_yfinance_data(tickers)
    # ticker_scraper.validate_data(len(tickers))
