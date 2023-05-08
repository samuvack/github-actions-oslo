from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re

driver = webdriver.Chrome()

outputfile = '../output/dead_links.md'

file1 = open('./dead_link_urls.txt', 'r')
lines = file1.readlines()


def create_empty_file(filename):
    """
    Create an empty file.

    Args:
        filename (str): The name of the file to be created.

    Returns:
        None
    """
    try:
        with open(filename, 'w') as file:
            pass
        print(f'Success: Empty file "{filename}" created.')
    except IOError as e:
        print(f'Error: Failed to create empty file. {e}')


def write_to_file(filename, parameter):
    """
    Write a parameter to a file.

    Args:
        parameter (str): The parameter to be written.
        filename (str): The name of the file to write to.

    Returns:
        None
    """
    try:
        with open(filename, 'a') as file:
            file.write(parameter)
        print(
            f'Success: Parameter "{parameter}" written to file "{filename}".')
    except IOError as e:
        print(f'Error: Failed to write parameter to file. {e}')
    finally:
        file.close()



for line in lines:
        link = str(line) #'https://data.vlaanderen.be/standaarden/erkende-standaard/openbaar-domein---uitbreiding-begraafplaats-(vocabularium).html'
        #print(link)
        #write_to_file(outputfile, '\n')
        #write_to_file(outputfile, '\n')
        #write_to_file(outputfile, '\n')
        #write_to_file(outputfile, link)
        #write_to_file(outputfile, '\n')

        def substring_after(s, delim):
            return s.partition(delim)[1]


        def validate_url(url):
            try:
                r = requests.head(url)
                if str(r.status_code) == '404':
                    return True
            except IOError as e:
                return True


        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = []
        url_names = []

        for link in soup.find_all('a'):
            print(link.get('href'))
            if 'http' in link.get('href'):
                urls.append(link.get('href'))


        print(urls)


        text = ''

        for i in range(0, len(urls)):
            if validate_url(urls[i]):
                if text == '':
                    text += '\n'
                    text += '\n'
                    text += '\n'
                    text += str(line)
                    text += '\n'

                print('url is broken (' + str(urls[i]) + ')')
                text += 'url is broken (' + str(urls[i]) + ')'
                text += '\n'
                #write_to_file(outputfile, 'url is broken (' + urls[i] + ')')
                #write_to_file(outputfile, '\n')
        write_to_file(outputfile, str(text))
        write_to_file('../log/checked.txt', str(line))

        