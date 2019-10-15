import requests
from bs4 import BeautifulSoup
import script_scraping as ScrapingService

def scrape_html():
    page = requests.get(ScrapingService.url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup