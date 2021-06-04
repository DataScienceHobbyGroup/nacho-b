"""TODO: Add file description."""

# Import third-party modules
import pandas as pd
import requests
from bs4 import BeautifulSoup


class Scraper:
    """TODO: Add classs description."""

    try:
        def scrape(website=None, _class=None):
            """TODO: Add descriotion."""
            if not (website and _class) is None:
                try:
                    page = requests.get(website)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    _classes = soup.find_all(class_=_class)
                    tickers = [tick.text for tick in _classes]
                    data = {'Tickers': tickers}
                    info = pd.DataFrame(data, columns=['Tickers'])
                    return tickers  # info['Tickers']
                except Exception:
                    print('Failed to scrape')
            else:
                print(f'invalid arguement: {website} or {_class}')
    except Exception:
        print('Initial Error: Couldn\'t scrape it')
