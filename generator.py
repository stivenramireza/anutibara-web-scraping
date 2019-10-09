from secrets import Secrets
import json

class Generator():

    def __init__(self):
        super().__init__()

    def create_json(self, id_property, json_data):
        document = 'property_' + str(id_property)
        try:
            with open('./' + Secrets.PATH_JSON + '/' + document + '.json', 'w') as outfile:
                json.dump(json_data, outfile, indent = 4, ensure_ascii = False)
                print("JSON document " + document + " generated successfully")
        except:
            print("Error to generate JSON document")