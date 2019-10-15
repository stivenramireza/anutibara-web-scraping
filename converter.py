import crawl
import generator
import json, re

def convert_string_to_json(url):
    soup = crawl.scrape_html()
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

def convert_new_property_to_json(json_property_agency, property_location, owner_property, property_features, property_hidden_features, array_offers_type):
    new_property_dict = {
        'code': int(json_property_agency["AdvertId"]),
        'status': json_property_agency["Status"],
        'type': json_property_agency["TransactionType"],
        'use': 'Nuevo',
        'modifyDate': json_property_agency["ModifyDate"],
        'nameProject': json_property_agency["Title"],
        'location': property_location,
        'builderCompany': owner_property,
        'description': json_property_agency["Description"],
        'features': property_features,
        'moreFeatures': property_hidden_features,
        'offersType': array_offers_type[1:]
    }
    generator.create_json(new_property_dict)

def convert_old_property_to_json(json_property_agency, property_location, owner_property, property_features, property_hidden_features):
    old_property_dict = {
        'code': int(json_property_agency["AdvertId"]),
        'status': json_property_agency["Status"],
        'type': json_property_agency["TransactionType"],
        'use': 'Usado',
        'modifyDate': json_property_agency["ModifyDate"],
        'location': property_location,
        'propertyAgency': owner_property,
        'description': json_property_agency["Description"],
        'features': property_features,
        'moreFeatures': property_hidden_features
    }
    generator.create_json(old_property_dict)