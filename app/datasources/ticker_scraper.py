from app.datasources.scraper import scraper
import yfinance as yf

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
  # ticker_data = []
  # for i in range(4):
  #   ticker_data.append(yf.Ticker(list_of_tickers[i]))
  # for td in ticker_data:  
  #   print(td.info)

# Entrypoint
if __name__ == '__main__':
  ts = TickerScraper()
  ts.read_in_site_list('resources/sites.txt')