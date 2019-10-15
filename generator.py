import secrets
import json

def create_json(id_property, json_data):
    document = 'property_' + str(id_property)
    try:
        with open('./generated_json/' + document + '.json', 'w') as outfile:
            json.dump(json_data, outfile, indent = 4, ensure_ascii = False)
            print("JSON document " + document + " generated successfully")
    except:
        print("Error to generate JSON document")