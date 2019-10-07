from crawl import Crawl
from scraper import Scraper

import settings

def main():
    settings.init() 
    Crawl()
    Scraper()

if __name__ == '__main__':
    main()