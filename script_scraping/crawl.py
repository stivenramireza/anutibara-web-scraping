import requests
from bs4 import BeautifulSoup
import settings

class Crawl():

    def __init__(self):
        super().__init__()

    def scrape_html(self):
        page = requests.get(settings.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup