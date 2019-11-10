from bs4 import BeautifulSoup
import requests, re, secrets

def request_properties(pages_list):
    properties_pages_list = []
    for paginator in pages_list:
        page = requests.get(paginator)
        soup = BeautifulSoup(page.content, 'html.parser')
        division = soup.find(id='divAdverts')
        for i in range(0, 34):
            properties = division.find(id='rowIndex_' + str(i))
            property = properties.find('li', class_='media').attrs.get('onclick')
            url_property = str(property).replace('javascript:window.location=', '')
            url_property = secrets.MAIN_URL + url_property.replace("'", "")
            properties_pages_list.append(url_property)
    return properties_pages_list