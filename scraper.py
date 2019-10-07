import requests, re, json
from bs4 import BeautifulSoup

class Scraper():

    """
        Inicialización de la clase Scraper
    """
    def __init__(self):
        super().__init__()
        self.extract_html()
        self.scrape_property()

    """
        Extrae el html de la url asignada
    """
    def extract_html(self):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    """
        Identifica si la url es de una propiedad nueva o vieja
        :url URL a analizar
    """
    def scrape_url(self, url):
        isNew = False
        url_scraped = url.split('-')
        url_scraped = " ".join(url_scraped)
        if(url_scraped.find("nuevo") != -1):
            isNew = True
        else:
            isNew = False
        return isNew

    """
        Extrae toda la información de una propiedad
    """
    def scrape_property(self):
        if(self.scrape_url(url)):   # Si es una propiedad nueva
            print("New property")
        else:                       # Si es una propiedad vieja
            print("Old property")

    """
        Extrae toda la información de una propiedad nueva
        :url Página a scrapear
        :json_finca_raiz JSON que entrega la página de Finca Raíz
    """
    def scrape_new_property(self, url, json_finca_raiz):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Extract Prices
        detail_header = soup.find('div', class_='row detailheader')
        detail_price = detail_header.find('div', class_='price')
        property_min_price = ''
        property_max_price = ''
        array_prices = []
        for price in detail_price.find_all('label'):
            array_prices.append(price.text)
        property_min_price = array_prices[0].split()
        property_min_price = " ".join(property_min_price)
        property_max_price = array_prices[1].split()
        property_max_price = " ".join(property_max_price)

        # Extract Builder Company
        builder_company = []
        builder_company_object = {
            'id': int(json_finca_raiz["ClientId"]),
            'builderCompany': json_finca_raiz["ClientName"],
            'contractType': json_finca_raiz["ContractType"],
            'schedule': json_finca_raiz["Schedule"]
        }
        builder_company.append(builder_company_object)

        # Extract Location
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

        # Estract Big Features
        property_features = []
        features_object = {
            'minPrice': property_min_price[2:],
            'maxPrice': property_max_price[2:],
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

        # Hidden Extra
        extra = soup.find('div', id='DivEstrasHidden')
        extras = []
        for h4 in extra.find_all('h4'):
            extras.append(h4.text)

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

        # Extract Offers Types
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

    """
        Extrae toda la información de una propiedad antigua
        :url Página a scrapear
        :json_finca_raiz JSON que entrega la página de Finca Raíz
    """
    def scrape_old_property(self, url, json_finca_raiz):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Extract Location
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

        # Extract Property Agency
        property_agency = []
        agency_object = {
            'id': int(json_finca_raiz["ClientId"]),
            'name': json_finca_raiz["ClientName"],
            'contractType': json_finca_raiz["ContractType"],
            
            'financing': json_finca_raiz["Financing"],
            'schedule': json_finca_raiz["Schedule"]
        }
        property_agency.append(agency_object)

        # Extract Big Features
        property_features = []
        features_object = {
            'price': json_finca_raiz["Price"],
            'squareMeters': json_finca_raiz['FormatedSurface'][0:-3],
            'rooms': int(json_finca_raiz['Rooms']),
            'bathrooms': int(json_finca_raiz['Baths']),
            'garages': json_finca_raiz['Garages'],
            'privateArea': json_finca_raiz['FormatedLivingArea'][0:-3],
            'constructionArea': json_finca_raiz['FormatedSurface'][0:-3],
            'squareMetersPrice': json_finca_raiz['PriceM2'],
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

        # Hidden Extra
        extra = soup.find('div', id='DivEstrasHidden')
        extras = []
        for h4 in extra.find_all('h4'):
            extras.append(h4.text)

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