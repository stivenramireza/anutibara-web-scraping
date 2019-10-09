import requests, settings
from bs4 import BeautifulSoup

class Crawl():

    def __init__(self):
        super().__init__()

    def scrape_html(self):
        page = requests.get(settings.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup