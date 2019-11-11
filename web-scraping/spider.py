import crawl

def extract_owner_property(json_property_agency):
    owner_property_object = {
        'id': int(json_property_agency["ClientId"]),
        'name': json_property_agency["ClientName"],
        'contractType': json_property_agency["ContractType"],
        'financing': json_property_agency["Financing"],
        'schedule': json_property_agency["Schedule"]
    }
    return owner_property_object

def extract_location(json_property_agency):
    location_object = {
        'country': 'Colombia',
        'department': 'Antioquia',
        'city': 'Medellin',
        'sector': json_property_agency["Location3"],
        'neighborhood': json_property_agency["Neighborhood"],
        'address': json_property_agency["Address"],
        'latitude': float(json_property_agency["Latitude"]),
        'longitude': float(json_property_agency["Longitude"])
    }
    return location_object

def extract_big_features(json_property_agency):
    features_object = {
        'price': json_property_agency['FormatedPrice'],
        'squareMeters': json_property_agency['FormatedSurface'][0:-3],
        'rooms': int(json_property_agency['Rooms']),
        'bathrooms': int(json_property_agency['Baths']),
        'garages': json_property_agency['Garages'],
        'privateArea': json_property_agency['FormatedLivingArea'][0:-3],
        'constructionArea': json_property_agency['FormatedSurface'][0:-3],
        'squareMetersPrice': float(json_property_agency['PriceM2']),
        'stratum': json_property_agency['Stratum'],
        'condition': json_property_agency['Condition'],
        'antiquity': json_property_agency['Ages'],
        'floor': json_property_agency['FloorId'],
        'interiorFloors': int(json_property_agency['InteriorFloors']),
        'weather': json_property_agency['Weather'],
        'includesAdministration': json_property_agency['IncludesAdministration'],
        'admonPrice': float(json_property_agency['AdministrationPrice'])
    }
    return features_object

def extract_hidden_extra(url):
    soup = crawl.scrape_html(url)
    hidden_extra_object = dict()
    if(soup.find('div', id='DivEstrasHidden') == None):
        hidden_extra_object = ""
    else:
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
        
        hidden_extra_object = {
            'interiorFeatures': property_interior_features,
            'exteriorFeatures': property_exterior_features,
            'sectorFeatures': property_sector_features
        }
    return hidden_extra_object

def extract_offers_type(url):
    soup = crawl.scrape_html(url)
    array_offers_type = []
    if(soup.find('div', id='typology') == None):
        array_offers_type.append('')
    else:
        offers_type = soup.find('div', id='typology')
        table = offers_type.find('table')
        
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
                'areaOfferType': area,
                'privateAreaOfferType': private_area,
                'roomsOfferType': rooms,
                'bathroomsOfferType': baths,
                'priceOfferType': price
            }
            array_offers_type.append(table_object)
    return array_offers_type