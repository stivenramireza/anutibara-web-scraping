import requests, re, json
from bs4 import BeautifulSoup
from crawl import Crawl
import settings

class Converter():

    def __init__(self):
        super().__init__()
        self.crawl = Crawl()

    def convert_string_to_json(self, url):
        soup = self.crawl.scrape_html()
        pattern = re.compile("var sfAdvert = \{.*\:.*\:.*\};")
        json_property = ''
        for script in soup.find_all("script", type="text/javascript"):
            if(pattern.findall(script.text)):
                json_property = pattern.findall(script.text)[0].split()[3:]
                json_to_strip = (json_property[-1])[0:-1]
                json_property = json_property[0:-1]
                json_property.append(json_to_strip)
                json_property = " ".join(json_property)

        json_finca_raiz = json.loads(json_property)
        return json_finca_raiz
    
    def convert_new_property_to_json(self, json_finca_raiz, property_location, owner_property, property_features, property_hidden_features, array_offers_type):
        new_property_dict = {
            'code': json_finca_raiz["AdvertId"],
            'status': json_finca_raiz["Status"],
            'type': json_finca_raiz["TransactionType"],
            'use': 'Nuevo',
            'modifyDate': json_finca_raiz["ModifyDate"],
            'nameProject': json_finca_raiz["Title"],
            'location': property_location,
            'builderCompany': owner_property,
            'description': json_finca_raiz["Description"],
            'features': property_features,
            'moreFeatures': property_hidden_features,
            'offersType': array_offers_type[1:]
        }
        print(json.dumps(new_property_dict, indent=4))

    def convert_old_property_to_json(self, json_finca_raiz, property_location, owner_property, property_features, property_hidden_features):
        old_property_dict = {
            'code': int(json_finca_raiz["AdvertId"]),
            'status': json_finca_raiz["Status"],
            'type': json_finca_raiz["TransactionType"],
            'use': 'Usado',
            'modifyDate': json_finca_raiz["ModifyDate"],
            'location': property_location,
            'propertyAgency': owner_property,
            'description': json_finca_raiz["Description"],
            'features': property_features,
            'moreFeatures': property_hidden_features
        }
        print(json.dumps(old_property_dict, indent=4))