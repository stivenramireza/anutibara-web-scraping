import crawl
import scraper
import settings

def main():
    settings.init()
    crawl.scrape_html()
    scraper.scrape_property()

if __name__ == '__main__':
    main()