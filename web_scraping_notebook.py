# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% [markdown]
# ## Pages List (Buy)

#%%
# Pages List (Buy)
import requests
from bs4 import BeautifulSoup

pages_list = []
for i in range(1, 839):
    pages_list.append('https://www.fincaraiz.com.co/finca-raiz/venta/medellin/?ad=30|'+ str(i) +'||||1||8,9,3,4,22,2,5,7,19,23,21,18,20|||55|5500006||||||||||||||||1|||1||griddate%20desc||||-1||')
    print('Paginator #' + str(i) + ": " + pages_list[i-1])

#%% [markdown]
# ## Properties Pages List (Buy)

#%%
# Properties Pages List (Buy)
paginator_url = 'https://www.fincaraiz.com.co/finca-raiz/venta/medellin/?ad=30|1||||1||8,9,3,4,22,2,5,7,19,23,21,18,20|||55|5500006||||||||||||||||1|||1||griddate%20desc||||-1||'
page = requests.get(paginator_url)
soup = BeautifulSoup(page.content, 'html.parser')
division = soup.find(id='divAdverts')
properties_pages_list = []
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
    print('Property #' + str(i) + ": " + str(url_property))
    #properties_pages_list.append(url_property)

#%%
