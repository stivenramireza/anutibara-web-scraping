import crawl
import spider
import converter
import settings

def scrape_url(url):
    is_new = False
    url_scraped = settings.url.split('-')
    url_scraped = " ".join(url_scraped)
    if(url_scraped.find("nuevo") != -1):
        is_new = True
    else:
        is_new = False
    return is_new

def scrape_property():
    is_new = scrape_url(settings.url)
    json_property_agency = converter.convert_string_to_json(settings.url)
    property_location = spider.extract_location(json_property_agency)
    owner_property = spider.extract_owner_property(json_property_agency)
    property_features = spider.extract_big_features(json_property_agency)
    property_hidden_features = spider.extract_hidden_extra()
    
    if(is_new): # Si es una propiedad nueva
        array_offers_type = spider.extract_offers_type()
        converter.convert_new_property_to_json(
            json_property_agency,
            property_location,
            owner_property,
            property_features,
            property_hidden_features,
            array_offers_type
        )
    else: # Si es una propiedad vieja
        converter.convert_old_property_to_json(
            json_property_agency,
            property_location,
            owner_property,
            property_features,
            property_hidden_features
        )