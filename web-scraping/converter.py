import crawl
import generator
from datetime import datetime
import json, re

date = datetime.now()
scraping_date = str(date.strftime("%d")) + '/' + str(date.strftime("%m")) + '/' + str(date.strftime("%Y"))
scraping_hour = str(date.strftime("%X"))

def convert_string_to_json(url):
    soup = crawl.scrape_html(url)
    pattern = re.compile("var sfAdvert = \{.*\:.*\:.*\};")
    json_property = ''
    for script in soup.find_all("script", type="text/javascript"):
        if(pattern.findall(script.text)):
            json_property = pattern.findall(script.text)[0].split()[3:]
            json_to_strip = (json_property[-1])[0:-1]
            json_property = json_property[0:-1]
            json_property.append(json_to_strip)
            json_property = " ".join(json_property)

    json_property_agency = json.loads(json_property)
    return json_property_agency

def convert_12_to_24(str1): 
    if str1[-2:] == "AM" and str1[:2] == "12": 
        return "00" + str1[2:-2] 
    elif str1[-2:] == "AM": 
        return str1[:-2] 
    elif str1[-2:] == "PM" and str1[:2] == "12": 
        return str1[:-2] 
    else: 
        return str(int(str1[:2]) + 12) + str1[2:8] 

def convert_new_property_to_json(json_property_agency, property_location, owner_property, property_features, property_hidden_features, array_offers_type, url):
    modify_date = json_property_agency["ModifyDate"].split()[0]
    modify_date = modify_date.split('/')
    modify_date = modify_date[1] + '/' + modify_date[0] + '/' + modify_date[2]
    modify_date_object = datetime.strptime(modify_date, '%d/%m/%Y')
    modify_date = datetime.strftime(modify_date_object, '%d/%m/%Y')
  
    hour = json_property_agency["ModifyDate"].split()[1]
    am_pm = json_property_agency["ModifyDate"].split()[2]
    modify_hour_object = datetime.strptime(hour, '%H:%M:%S')
    modify_hour_str = datetime.strftime(modify_hour_object, '%H:%M:%S')
    modify_hour = modify_hour_str + " " + am_pm
    modify_hour = convert_12_to_24(modify_hour)

    array_interior_features = ''
    array_exterior_features = ''
    array_sector_features = ''
    for key in property_hidden_features:
        if(key == 'interiorFeatures'):
            array_interior_features = property_hidden_features[key]
        elif(key == 'exteriorFeatures'):
            array_exterior_features = property_hidden_features[key]
        else:
            array_sector_features = property_hidden_features[key]

    new_property_dict = {
        'urlProperty': url,
        'scrapingDate': scraping_date,
        'scrapingHour': scraping_hour,
        'modifyDate': modify_date,
        'modifyHour': modify_hour,
        'code': int(json_property_agency["AdvertId"]),
        'status': json_property_agency["Status"],
        'type': json_property_agency["TransactionType"],
        'use': 'Nuevo',
        'nameProject': json_property_agency["Title"],
        'country': property_location['country'],
        'department': property_location['department'],
        'city': property_location['city'],
        'sector': property_location['sector'],
        'neighborhood': property_location['neighborhood'],
        'address': property_location['address'],
        'latitude': property_location['latitude'],
        'longitude': property_location['longitude'],
        'idOwnerProperty': owner_property['id'],
        'nameOwnerProperty': owner_property['name'],
        'contractType': owner_property['contractType'],
        'financing': owner_property['financing'],
        'schedule': owner_property['schedule'],
        'description': json_property_agency["Description"],
        'price': property_features['price'],
        'squareMeters': property_features['squareMeters'],
        'rooms': property_features['rooms'],
        'bathrooms': property_features['bathrooms'],
        'garages': property_features['garages'],
        'privateArea': property_features['privateArea'],
        'constructionArea': property_features['constructionArea'],
        'squareMetersPrice': property_features['squareMetersPrice'],
        'stratum': property_features['stratum'],
        'condition': property_features['condition'],
        'antiquity': property_features['antiquity'],
        'floor': property_features['floor'],
        'interiorFloors': property_features['interiorFloors'],
        'weather': property_features['weather'],
        'includesAdministration': property_features['includesAdministration'],
        'admonPrice': property_features['admonPrice'],
        'interiorFeatures': array_interior_features,
        'exteriorFeatures': array_exterior_features,
        'sectorFeatures': array_sector_features,
        'offersType': array_offers_type[1:]
    }
    generator.create_json(new_property_dict)

def convert_old_property_to_json(json_property_agency, property_location, owner_property, property_features, property_hidden_features, array_offers_type, url):
    modify_date = json_property_agency["ModifyDate"].split()[0]
    modify_date = modify_date.split('/')
    modify_date = modify_date[1] + '/' + modify_date[0] + '/' + modify_date[2]
    modify_date_object = datetime.strptime(modify_date, '%d/%m/%Y')
    modify_date = datetime.strftime(modify_date_object, '%d/%m/%Y')
    
    hour = json_property_agency["ModifyDate"].split()[1]
    am_pm = json_property_agency["ModifyDate"].split()[2]
    modify_hour_object = datetime.strptime(hour, '%H:%M:%S')
    modify_hour_str = datetime.strftime(modify_hour_object, '%H:%M:%S')
    modify_hour = modify_hour_str + " " + am_pm
    modify_hour = convert_12_to_24(modify_hour)

    array_interior_features = []
    array_exterior_features = []
    array_sector_features = []
    for key in property_hidden_features:
        if(key == 'interiorFeatures'):
            array_interior_features.append(property_hidden_features[key])
        elif(key == 'exteriorFeatures'):
            array_exterior_features.append(property_hidden_features[key])
        else:
            array_sector_features.append(property_hidden_features[key])

    old_property_dict = {
        'urlProperty': url, 
        'scrapingDate': scraping_date,
        'scrapingHour': scraping_hour,
        'modifyDate': modify_date,
        'modifyHour': modify_hour,
        'code': int(json_property_agency["AdvertId"]),
        'status': json_property_agency["Status"],
        'type': json_property_agency["TransactionType"],
        'use': 'Usado',
        'nameProject': json_property_agency["Title"],
        'country': property_location['country'],
        'department': property_location['department'],
        'city': property_location['city'],
        'sector': property_location['sector'],
        'neighborhood': property_location['neighborhood'],
        'address': property_location['address'],
        'latitude': property_location['latitude'],
        'longitude': property_location['longitude'],
        'idOwnerProperty': owner_property['id'],
        'nameOwnerProperty': owner_property['name'],
        'contractType': owner_property['contractType'],
        'financing': owner_property['financing'],
        'schedule': owner_property['schedule'],
        'description': json_property_agency["Description"],
        'price': property_features['price'],
        'squareMeters': property_features['squareMeters'],
        'rooms': property_features['rooms'],
        'bathrooms': property_features['bathrooms'],
        'garages': property_features['garages'],
        'privateArea': property_features['privateArea'],
        'constructionArea': property_features['constructionArea'],
        'squareMetersPrice': property_features['squareMetersPrice'],
        'stratum': property_features['stratum'],
        'condition': property_features['condition'],
        'antiquity': property_features['antiquity'],
        'floor': property_features['floor'],
        'interiorFloors': property_features['interiorFloors'],
        'weather': property_features['weather'],
        'includesAdministration': property_features['includesAdministration'],
        'admonPrice': property_features['admonPrice'],
        'interiorFeatures': array_interior_features,
        'exteriorFeatures': array_exterior_features,
        'sectorFeatures': array_sector_features,
        'offersType': array_offers_type[1:]
    }
    generator.create_json(old_property_dict)