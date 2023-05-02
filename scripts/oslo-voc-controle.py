from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re

driver = webdriver.Chrome()

link = 'https://data.vlaanderen.be/standaarden/erkende-standaard/openbaar-domein---uitbreiding-begraafplaats-(vocabularium).html'

def substring_after(s, delim):
    return s.partition(delim)[1]

def validate_url(url):
    r = requests.head(url)
    if str(r.status_code) == '404':
        return True

response = requests.get(link)
soup = BeautifulSoup(response.text, 'html.parser')
urls = []
url_names = []

for link in soup.find_all('a'):
    print(link.get('href'))
    if 'http' in link.get('href'):
        urls.append(link.get('href').split(' ')[0])
        if ' ' in link.get('href'):
            url_names.append(link.get('href')[link.get('href').find(' '):])
        else:
            url_names.append('')

print(urls)
print(url_names)

for i in range(0, len(urls)):
    if validate_url(urls[i]):
        print(url_names[i] + ' is broken (' + urls[i] + ')')
