import requests, re, json
from bs4 import BeautifulSoup

class Generator():

    def __init__(self):
        super().__init__()

    def create_json(self, id_property, json_data):
        with open('./generated_json/property_' + str(id_property) + '.json', 'w') as outfile:
            json.dump(json_data, outfile, indent = 4, ensure_ascii=False)