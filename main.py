from scraper import Scraper
from converter import Converter

url = 'https://www.fincaraiz.com.co/aiana-verde/medellin/proyecto-nuevo-det-4837830.aspx?itemid=4837834'

"""
    Script que hace el scraping de una propiedad en especifico
    a través de su URL
"""
def main():
    Scraper()
    Converter()

if __name__ == '__main__':
    main()