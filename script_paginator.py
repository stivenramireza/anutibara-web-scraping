from bs4 import BeautifulSoup
from secrets import Secrets
import requests, re

def paginate_properties():
    pages_list_to_process = []
    main_page_url = Secrets.MAIN_PAGE_URL
    page = requests.get(main_page_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    pattern = re.compile("var totalPages = [\d]*;")
    total_pages = ''
    for script in soup.find_all("script", type="text/javascript"):
        if(pattern.findall(script.text)):
            total_pages = int((pattern.findall(script.text)[0].split()[-1])[0:-1])
    for i in range(1, total_pages + 1):
        pages_list_to_process.append(Secrets.MAIN_PAGE_SHORT_URL + '/?ad=30|'+ str(i) +'||||1||8,9,3,4,22,2,5,7,19,23,21,18,20|||55|5500006||||||||||||||||1|||1||griddate%20desc||||-1||')
    return pages_list_to_process

def main():
    paginate_properties()

if __name__ == "__main__":
    main()