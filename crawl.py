import requests, settings
from bs4 import BeautifulSoup

def scrape_html():
    page = requests.get(settings.url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup