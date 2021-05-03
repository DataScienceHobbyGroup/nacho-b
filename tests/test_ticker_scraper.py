import unittest
import importlib
import re

from app.datasources.ticker_scraper import TickerScraper

class Testing(unittest.TestCase):
  VALID_URL = r'(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?'
  ts = TickerScraper()

  def test_read_in_site_list(self):
    print('\nTesting read in site list....\n')
    list_of_sites = self.ts.read_in_site_list('resources/sites.txt')
    print('Type is a list')
    self.assertEqual(type(list_of_sites), type([]))
    print('list is not empty')
    self.assertTrue(len(list_of_sites) > 0)
    print('values in list are valid urls')
    for site in list_of_sites:
      self.assertTrue(len(re.findall(self.VALID_URL, site)) > 0)
    print('Finished testing read in site lists')
  
  def test_scrape_tickers(self):
    print('\nTesting scrape tickers....\n')
    list_of_tickers = self.ts.scrape_tickers(self.ts.read_in_site_list('resources/sites.txt'))
    print('type is a list')
    self.assertEqual(type(list_of_tickers), type([]))
    print('list is not empty')
    self.assertTrue(len(list_of_tickers) > 0)
    print('contains valid tickers', list_of_tickers)
    self.assertIn('BTC-USD', list_of_tickers)
    print('Finished testing scrape tickers')

if __name__ == '__main__':
  unittest.main()