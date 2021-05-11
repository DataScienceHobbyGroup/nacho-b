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

  # save scraped data
  def save_data(self, list_of_tickers=None):
    ticker_data = pd.DataFrame() # (yf.Ticker("MSFT")).info)
    # print(ticker_data.head())
    startDate = ''
    dateRanges = []
    # get the errors from yfinance which give the starting point of data
    # create a list of lists with start and end values
    #for tick in list_of_tickers:
    for i in range(4):
      # a_ticker = yf.Ticker(tick)
      a_ticker = yf.Ticker(list_of_tickers[i])
      # info = a_ticker.info
      (a_ticker.history(period='max', interval='3mo'))# .to_csv(f'./data/{tick}_data.txt')
      # startDate = util.parse_historical_start_date(yf.shared._ERRORS[tick])
      startDate = util.parse_historical_start_date(yf.shared._ERRORS[list_of_tickers[i]])
      dateRanges.append(util.calculate_time_periods_for_ticker(startDate))
      # ticker_data[f'{list_of_tickers[i]}_info'] = pd.Series(info)
      # ticker_data[f'{list_of_tickers[i]}_history'] = pd.Series(history)
    # print(ticker_data.head())
    
    # for each currency get 1m data for the correct start to end time using the limiter to stay under the API limit
    for ranges in dateRanges:
      for range_ in ranges:
        # (a_ticker.history(start=range_['start'], end=range_['end'], interval='1m')).to_csv(f'./data/{tick}_data.txt', mode='a')
        (a_ticker.history(start=range_['start'], end=range_['end'], interval='1m')).to_csv(f'./data/{list_of_tickers[i]}_data.txt', mode='a')

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



    # with open('data.txt', 'w') as file:
    #   # file.write(info)
    #   file.write(history)
    # with open('data.txt', 'w') as file:      
    #   for td in ticker_data:
    #     file.write(str(td))

# Entrypoint
if __name__ == '__main__':
  ticker_scraper = TickerScraper()
  list_of_sites = ticker_scraper.read_in_site_list('resources/sites.txt')
  tickers = ticker_scraper.scrape_tickers(list_of_sites)
  ticker_scraper.download_yfinance_data(tickers)