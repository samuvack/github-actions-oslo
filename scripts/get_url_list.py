import re
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor



driver = webdriver.Chrome()

link = 'https://data.vlaanderen.be/standaarden/statistics'


response = requests.get(link)
soup = BeautifulSoup(response.text, 'html.parser')
urls = []
url_names = []

for link in soup.find_all('a'):
    print(link.get('href'))
    if 'http' in link.get('href'):
        urls.append(link.get('href').split(' ')[0])

print(urls)