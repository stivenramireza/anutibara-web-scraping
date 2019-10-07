import requests
import re
import json
from bs4 import BeautifulSoup

"""
    Convierte el string del JSON de Finca Raíz
    :url Página a buscar el JSON
"""
def convert_String_to_JSON(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

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
    Script que hace el scraping de una propiedad en especifico
    a través de su URL
"""
def main():
    url = 'https://www.fincaraiz.com.co/aiana-verde/medellin/proyecto-nuevo-det-4837830.aspx?itemid=4837834'
    convert_String_to_JSON(url)

if __name__ == "__main__":
    main()