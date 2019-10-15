import secrets
import crawl
import scraper

def scrape(url_to_scrape):
    global url
    url = url_to_scrape
    crawl.scrape_html()
    scraper.scrape_property()