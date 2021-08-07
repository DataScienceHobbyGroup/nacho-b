"""
Container for scraping logic.

Date: 2021
Author: Barry Foye
"""

# Import third-party modules
import requests
from bs4 import BeautifulSoup


class Scraper:
    """
    This class is used to scrape data and information from websites.

    It is a container for any bespoke logic related to a particular site
    and the nuances for that site.

    TODO: Currently this class is written with a bias to scraping a
    specific class from a specific website. This can be improved to
    handle multiple scenarios like multiple classes or other DOM elements.
    """

    try:
        def scrape(website=None, _class=None):
            """Scrape a website for a given class."""
            if not (website and _class) is None:
                try:
                    page = requests.get(website)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    _classes = soup.find_all(class_=_class)
                    tickers = [tick.text for tick in _classes]
                    return tickers
                except Exception:
                    print('Failed to scrape')
            else:
                print(f'invalid arguement: {website} or {_class}')
    except Exception:
        print('Initial Error: Couldn\'t scrape it')
