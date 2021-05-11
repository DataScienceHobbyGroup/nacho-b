try:
  from .scraper import scraper
except ImportError:
  from scraper import scraper

import yfinance as yf
import pandas as pd
try:
  from .util import util as util
except ImportError:
  import util as util

class TickerScraper:
  YAHOO_FINANCE_TICKER_CLASS = 'Fw(600) C($linkColor)'  
  # read in site list
  def read_in_site_list(self, file=None):
    sites_urls = open(file)
    list_of_sites = sites_urls.read().split('\n')
    sites_urls.close()
    return list_of_sites
  # scrape tickers
  def scrape_tickers(self, list_of_sites=None):
    list_of_tickers = []
    for s in list_of_sites:
      list_of_tickers.extend(scraper.scrape(s, self.YAHOO_FINANCE_TICKER_CLASS))
    return list_of_tickers
  # download yahoo finance data
  def download_yfinance_data(self, list_of_tickers=None):
    for tick in list_of_tickers:
      a_ticker = yf.Ticker(tick)
      for interval in util.INTERVALS:
        interval_ = util.date_range(interval)
        if 'error' in interval_:
          break
        elif 'period' in interval_:
          a_ticker.history(period=interval_['period'], interval=interval_['interval']).to_csv(f'./data/{tick}_data_{interval_["interval"]}.csv', mode='w')
        elif 'start' in interval_ and 'end' in interval_:
          a_ticker.history(start=interval_['start'], end=interval_['end'], interval=interval_['interval']).to_csv(f'./data/{tick}_data_{interval_["interval"]}.csv', mode='w')
        else:
          print('Some bogus shit going on here')
          break
        util.rate_limiter()
# Entrypoint
if __name__ == '__main__':
  ticker_scraper = TickerScraper()
  list_of_sites = ticker_scraper.read_in_site_list('resources/sites.txt')
  tickers = ticker_scraper.scrape_tickers(list_of_sites)
  ticker_scraper.download_yfinance_data(tickers)