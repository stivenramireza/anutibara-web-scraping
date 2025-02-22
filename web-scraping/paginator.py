from bs4 import BeautifulSoup
import secrets
import requests, re

headers={
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

def paginate_properties():
    pages_list_to_process = []
    
    # Properties to Buy
    main_page_url_buy = secrets.MAIN_PAGE_URL_BUY
    page_buy = requests.get(main_page_url_buy, headers = headers)
    soup_buy = BeautifulSoup(page_buy.text, 'html.parser')
    total_pages_buy = ''
    
    # Properties to Rent
    main_page_url_rent = secrets.MAIN_PAGE_URL_RENT
    page_rent = requests.get(main_page_url_rent, headers = headers)
    soup_rent = BeautifulSoup(page_rent.text, 'html.parser')
    total_pages_rent = ''
    
    pattern = re.compile("var totalPages = [\d]*;")
    for script in soup_buy.find_all("script", type="text/javascript"):
        if(pattern.findall(script.text)):
            total_pages_buy = int((pattern.findall(script.text)[0].split()[-1])[0:-1])
    for script in soup_rent.find_all("script", type="text/javascript"):
        if(pattern.findall(script.text)):
            total_pages_rent = int((pattern.findall(script.text)[0].split()[-1])[0:-1])
    for i in range(1, total_pages_buy + 1):
        pages_list_to_process.append(secrets.MAIN_PAGE_SHORT_URL_BUY + '/?ad=30|'+ str(i) +'||||1||8,9,3,4,22,2,5,7,19,23,21,18,20|||55|5500006||||||||||||||||1|||1||griddate%20desc||||-1||')
    for i in range(1, total_pages_rent + 1):
        pages_list_to_process.append(secrets.MAIN_PAGE_SHORT_URL_RENT + '/?ad=30|'+ str(i) +'||||2||8,9,3,4,22,2,5,7,19,23,21,18,20|||55|5500006||||||||||||||||1|||1||griddate%20desc||||-1||')
    return pages_list_to_process