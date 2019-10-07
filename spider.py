import requests, re, json
from bs4 import BeautifulSoup
import settings
from crawl import Crawl

class Spider():

    def __init__(self):
        super().__init__()
        self.crawl = Crawl()

    def extract_owner_property(self, json_finca_raiz):
        owner_property = []
        owner_property_object = {
            'id': int(json_finca_raiz["ClientId"]),
            'builderCompany': json_finca_raiz["ClientName"],
            'contractType': json_finca_raiz["ContractType"],
            'financing': json_finca_raiz["Financing"],
            'schedule': json_finca_raiz["Schedule"]
        }
        owner_property.append(owner_property_object)
        return owner_property
    
    def extract_location(self, json_finca_raiz):
        property_location = []
        location_object = {
            'country': 'Colombia',
            'department': 'Antioquia',
            'city': 'Medellin',
            'sector': json_finca_raiz["Location3"],
            'neighborhood': json_finca_raiz["Neighborhood"],
            'address': json_finca_raiz["Address"],
            'latitude': float(json_finca_raiz["Latitude"]),
            'longitude': float(json_finca_raiz["Longitude"])
        }
        property_location.append(location_object)
        return property_location

    def extract_big_features(self, json_finca_raiz):
        property_features = []
        features_object = {
            'price': json_finca_raiz['FormatedPrice'],
            'squareMeters': json_finca_raiz['FormatedSurface'][0:-3],
            'rooms': int(json_finca_raiz['Rooms']),
            'bathrooms': int(json_finca_raiz['Baths']),
            'garages': json_finca_raiz['Garages'],
            'privateArea': json_finca_raiz['FormatedLivingArea'][0:-3],
            'constructionArea': json_finca_raiz['FormatedSurface'][0:-3],
            'squareMetersPrice': float(json_finca_raiz['PriceM2']),
            'stratum': int(json_finca_raiz['Stratum']),
            'condition': json_finca_raiz['Condition'],
            'antiquity': json_finca_raiz['Ages'],
            'floors': json_finca_raiz['Floor'],
            'interiorFloors': int(json_finca_raiz['InteriorFloors']),
            'weather': json_finca_raiz['Weather'],
            'includesAdministration': json_finca_raiz['IncludesAdministration'],
            'admonPrice': float(json_finca_raiz['AdministrationPrice'])
        }
        property_features.append(features_object)
        return property_features

    def extract_hidden_extra(self):
        soup = self.crawl.scrape_html()
        extra = soup.find('div', id='DivEstrasHidden')
        extras = []
        for h4 in extra.find_all('h4'):
            extras.append(h4.text)
        array_hidden_extra = []
        property_interior_features = []
        property_exterior_features = []
        property_sector_features = []

        for extra in extras:
            if(extra.find('Caracteristicas Interiores') == 0): # Extract Interior Features
                interior_features = soup.find('ul', id='tblInitialInteriores')
                property_interior_features = [li.text for li in interior_features.find_all('li')]
            elif(extra.find('Caracteristicas Exteriores') == 0): # Extract Exterior Features
                exterior_features = soup.find('ul', id='tblInitialExteriores')
                property_exterior_features = [li.text for li in exterior_features.find_all('li')]
            elif(extra.find('Caracteristicas del Sector') == 0): # Extract Sector Features
                sector_features = soup.find('ul', id='tblInitialdelSector')
                property_sector_features = [li.text for li in sector_features.find_all('li')]
        
        hidden_extra_object = {
            'interiorFeatures': property_interior_features,
            'exteriorFeatures': property_exterior_features,
            'sectorFeatures': property_sector_features
        }
        array_hidden_extra.append(hidden_extra_object)
        return array_hidden_extra
    
    def extract_offers_type(self):
        soup = self.crawl.scrape_html()
        offers_type = soup.find('div', id='typology')
        table = offers_type.find('table')
        array_offers_type = []
        for tr in table.find_all('tr'):
            property = tr.find_all('td')[0].text.split()
            property = " ".join(property)
            offer_type = tr.find_all('td')[1].text.split()
            offer_type = " ".join(offer_type)
            area = tr.find_all('td')[2].text.split()
            area = " ".join(area)[0:-3].replace(",", ".")
            private_area = tr.find_all('td')[3].text.split()
            private_area = " ".join(private_area)[0:-3].replace(",", ".")
            rooms = tr.find_all('td')[4].text.split()
            rooms = " ".join(rooms)
            baths = tr.find_all('td')[5].text.split()
            baths = " ".join(baths)
            price = tr.find_all('td')[6].text.split()
            price = " ".join(price)[2:]
            
            table_object = {
                'property': property,
                'offerType': offer_type,
                'area': area,
                'privateArea': private_area,
                'rooms': rooms,
                'bathrooms': baths,
                'price': price
            }
            array_offers_type.append(table_object)
        return array_offers_type
    