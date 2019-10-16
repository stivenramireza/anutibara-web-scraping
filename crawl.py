import requests
from bs4 import BeautifulSoup

def scrape_html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup