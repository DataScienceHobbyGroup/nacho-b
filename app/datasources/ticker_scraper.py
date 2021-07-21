"""
Scraper for getting ticker data.

Date: 2021
Author: Barry Foye
"""

from app.datasources.scraper import scraper
import yfinance as yf


class TickerScraper:
    """Collection of functions to gather financial data."""

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

    def get_ticker_data(self, list_of_tickers=None):
        """Get scraped ticker data."""
        ticker_data = []
        for i in range(4):
            ticker_data.append(yf.Ticker(list_of_tickers[i]))

    def save_ticker_data(self, data=None):
        """Save data for later."""
        for td in data:
            print(td.info)
            # TODO: for integration we need a way to store the scraped data
            # in our DB.


# Entrypoint
if __name__ == '__main__':
    ts = TickerScraper()
    ts.read_in_site_list('resources/sites.txt')