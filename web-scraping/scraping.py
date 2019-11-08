import crawl
import scraper

def scrape(url_to_scrape):
    crawl.scrape_html(url_to_scrape)
    scraper.scrape_property(url_to_scrape)