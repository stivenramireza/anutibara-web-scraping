from multiprocessing import Pool
import script_paginator as PaginatorService
import script_properties as PropertyService
import script_scraping as ScrapingService
from time import sleep

def main():
    url_pages_list = []
    url_pages_list = PaginatorService.paginate_properties()
    url_properties_list = []
    url_properties_list = PropertyService.request_properties(url_pages_list)
    # Multiprocessing
    p = Pool(40)
    p.map(ScrapingService.scrape, url_properties_list)
    p.terminate()
    p.join()
    print('Scraping Service has finished successfully')

if __name__ == "__main__":
    main()
