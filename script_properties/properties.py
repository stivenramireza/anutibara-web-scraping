import requests, re
from bs4 import BeautifulSoup


def request_properties(properties_pages_list):
    paginator_url = 'https://www.fincaraiz.com.co/finca-raiz/venta/medellin/?ad=30|1||||1||8,9,3,4,22,2,5,7,19,23,21,18,20|||55|5500006||||||||||||||||1|||1||griddate%20desc||||-1||'
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

def main():
    pages_list = []
    pages_list = request_properties(pages_list)

if __name__ == "__main__":
    main()