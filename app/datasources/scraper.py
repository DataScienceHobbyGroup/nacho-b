import requests
from bs4 import BeautifulSoup

class scraper:
  try:
    def scrape(website=None, _class=None):
      if not (website and _class) == None:
        try:
          page = requests.get(website)
          soup = BeautifulSoup(page.content, 'html.parser')
          _classes = soup.find_all(class_ = _class)
          tickers = [tick.text for tick in _classes]
          data = {'Tickers':tickers}
          return tickers
        except:
          print('Failed to scrape')
      else:
        print(f'invalid arguement: {website} or {_class}')
  except:
    print('Initial Error: Couldn\'t scrape it')