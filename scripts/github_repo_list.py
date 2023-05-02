import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json

# setup owner name , access_token, and headers 
owner='samuvack'
access_token = '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'

i=1
while True:
    url = 'https://api.github.com/users/informatievlaanderen/repos?page='+str(i)
    response = requests.get(url, auth=(owner, access_token))
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
    if soup == '':
        break
    else:
        json_repos = json.loads(str(soup))
        print(json_repos)
        i = i+1

