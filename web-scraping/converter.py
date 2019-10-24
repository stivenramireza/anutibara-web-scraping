import crawl
import generator
import datetime as date
import json, re

date = date.datetime.now()
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

def convert_new_property_to_json(json_property_agency, property_location, owner_property, property_features, property_hidden_features, array_offers_type, url):
    modify_date = json_property_agency["ModifyDate"].split()[0]
    modify_hour = json_property_agency["ModifyDate"].split()[1:]
    modify_hour = " ".join(modify_hour)
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
        'location': property_location,
        'ownerProperty': owner_property,
        'description': json_property_agency["Description"],
        'features': property_features,
        'moreFeatures': property_hidden_features,
        'offersType': array_offers_type[1:]
    }
    generator.create_json(new_property_dict)

def convert_old_property_to_json(json_property_agency, property_location, owner_property, property_features, property_hidden_features, array_offers_type, url):
    modify_date = json_property_agency["ModifyDate"].split()[0]
    modify_hour = json_property_agency["ModifyDate"].split()[1:]
    modify_hour = " ".join(modify_hour)
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
        'location': property_location,
        'ownerProperty': owner_property,
        'description': json_property_agency["Description"],
        'features': property_features,
        'moreFeatures': property_hidden_features,
        'offersType': array_offers_type[1:]
    }
    generator.create_json(old_property_dict)