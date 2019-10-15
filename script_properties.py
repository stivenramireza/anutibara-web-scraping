from bs4 import BeautifulSoup
import requests, re, secrets

def request_properties(properties_pages_list, **kwargs):
    paginator_url = secrets.MAIN_PAGE_URL
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
        url_property = secrets.MAIN_URL + url_property.replace("'", "")
        properties_pages_list.append(url_property)
    return properties_pages_list