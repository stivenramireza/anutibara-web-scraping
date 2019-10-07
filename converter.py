import requests, re, json
from bs4 import BeautifulSoup
from scraper import Scraper

class Converter():

    """
        Inicialización de la clase Converter
    """
    def __init__(self):
        super().__init__()
        self.scraper = Scraper()
        self.convert_string_to_json(url)

    """
        Convierte el string del JSON de Finca Raíz
        :url Página a buscar el JSON
    """
    def convert_string_to_json(self, url):
        soup = self.scraper.extract_html()
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
    
    """
        Convertir la información del scraper  de la 
        propiedad nueva en JSON
    """
    def convert_old_property_to_json(self, json_finca_raiz, property_location, property_agency,property_features, property_interior_features, property_exterior_features, builder_company, property_sector_features, array_offers_type):
        new_property_dict = {
            'code': json_finca_raiz["AdvertId"],
            'status': json_finca_raiz["Status"],
            'type': json_finca_raiz["TransactionType"],
            'use': 'Nuevo',
            'modifyDate': json_finca_raiz["ModifyDate"],
            'nameProject': json_finca_raiz["Title"],
            'builderCompany': builder_company,
            'description': json_finca_raiz["Description"],
            'features': property_features,
            'interiorFeatures': property_interior_features,
            'exteriorFeatures': property_exterior_features,
            'sectorFeatures': property_sector_features,
            'offersType': array_offers_type[1:]
        }
        print(json.dumps(new_property_dict, indent=4))

    """
        Convertir la información del scraper  de la 
        propiedad nueva en JSON
    """
    def convert_new_property_to_json(self, json_finca_raiz, property_location, property_agency,property_features, property_interior_features, property_exterior_features, builder_company, property_sector_features, array_offers_type):
        old_property_dict = {
            'code': int(json_finca_raiz["AdvertId"]),
            'status': json_finca_raiz["Status"],
            'type': json_finca_raiz["TransactionType"],
            'use': 'Usado',
            'modifyDate': json_finca_raiz["ModifyDate"],
            'location': property_location,
            'propertyAgency': property_agency,
            'description': json_finca_raiz["Description"],
            'features': property_features,
            'interiorFeatures': property_interior_features,
            'exteriorFeatures': property_exterior_features,
            'sectorFeatures': property_sector_features,
        }
        print(json.dumps(old_property_dict, indent=4))