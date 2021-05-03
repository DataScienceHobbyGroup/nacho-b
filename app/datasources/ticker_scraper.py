from scraper import scraper
import yfinance as yf
# read in site list
sites_urls = open('app\\datasources\\sites.txt')
list_of_sites = sites_urls.read().split('\n')
sites_urls.close()
# scrape tickers
list_of_tickers = []
for s in list_of_sites:
  list_of_tickers.extend(scraper.scrape(s, 'Fw(600) C($linkColor)'))

ticker_data = []
for i in range(4):
  ticker_data.append(yf.Ticker(list_of_tickers[i]))
for td in ticker_data:  
  print(td.info)
