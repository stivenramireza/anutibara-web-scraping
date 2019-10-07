import requests, re, json
from bs4 import BeautifulSoup
import settings
from crawl import Crawl
from spider import Spider
from converter import Converter

class Scraper():

    def __init__(self):
        super().__init__()
        self.crawl = Crawl()
        self.spider = Spider()
        self.converter = Converter()
        self.scrape_property()

    def scrape_url(self, url):
        is_new = False
        url_scraped = settings.url.split('-')
        url_scraped = " ".join(url_scraped)
        if(url_scraped.find("nuevo") != -1):
            is_new = True
        else:
            is_new = False
        return is_new

    def scrape_property(self):
        is_new = self.scrape_url(settings.url)
        json_finca_raiz = self.converter.convert_string_to_json(settings.url)
        property_location = self.spider.extract_location(json_finca_raiz)
        owner_property = self.spider.extract_owner_property(json_finca_raiz)
        property_features = self.spider.extract_big_features(json_finca_raiz)
        property_hidden_features = self.spider.extract_hidden_extra()
        
        if(is_new): # Si es una propiedad nueva
            array_offers_type = self.spider.extract_offers_type()
            self.converter.convert_new_property_to_json(
                json_finca_raiz,
                property_location,
                owner_property,
                property_features,
                property_hidden_features,
                array_offers_type
            )
        else: # Si es una propiedad vieja
            self.converter.convert_old_property_to_json(
                json_finca_raiz,
                property_location,
                owner_property,
                property_features,
                property_hidden_features
            )