from multiprocessing import Pool
import paginator as PaginatorService
import properties as PropertyService
import scraping as ScrapingService
from time import sleep

def main():
    url_pages_list = []
    url_pages_list = PaginatorService.paginate_properties()
    url_properties_list = []
    url_properties_list = PropertyService.request_properties(url_pages_list)
    # Multiprocessing
    try:
        p = Pool(20)
        p.map(ScrapingService.scrape, url_properties_list)
        p.terminate()
        p.join()
        print('Scraping Service has finished successfully')
    except Exception as e:
        print('Error to scrape property: ', e)

if __name__ == "__main__":
    main()
