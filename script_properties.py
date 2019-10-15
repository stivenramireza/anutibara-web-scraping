from bs4 import BeautifulSoup
import requests, re

def request_properties(properties_pages_list, **kwargs):
    paginator_url = 'https://www.fincaraiz.com.co/finca-raiz/venta/medellin/?ad=30%7C1%7C%7C%7C%7C1%7C%7C8,9,3,4,22,2,5,7,19,23,21,18,20%7C%7C%7C55%7C5500006%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C1%7C%7C%7C1%7C%7Cgriddate%20desc%7C%7C%7C%7C-1%7C%7C'
    page = requests.get(paginator_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    properties_number = soup.find(id='lblNumInm').get_text()
    division = soup.find(id='divAdverts')
    for i in range(0, 34):
        properties = division.find(id='rowIndex_' + str(i))
        property = ''
        if (i == 0):
            property = properties.find('li', class_='media')
            property = property.find('span').attrs.get('onclick')
        else:
            property = properties.find('li', class_='media').attrs.get('onclick')
        url_property = str(property).replace('javascript:window.location=', '')
        url_property = 'https://www.fincaraiz.com.co' + url_property.replace("'", "")
        properties_pages_list.append(url_property)
    return properties_pages_list