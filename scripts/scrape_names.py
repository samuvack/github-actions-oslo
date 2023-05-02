from bs4 import BeautifulSoup
from selenium import webdriver
import json
import os
from pprintpp import pprint


def getLinks(driver):
    driver.get('https://data.vlaanderen.be/standaarden/')
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")

    dict = {}
    for tag in soup.find_all('a', href=True):
        titel = tag.text

        if "erkende-standaard" in tag['href'] or "kandidaat-standaard" in tag['href']:
            if tag['href'][:4] == "http":
                link = tag['href']
            else:
                link = "https://data.vlaanderen.be" + tag['href']

            dict[titel] = link
        
            print(link)
            write_to_file('./test.txt', str(link))
            write_to_file('./test.txt', '\n')

    return dict



def getStandaard(link, driver):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")

    lijst = []
    for art in soup.find_all('article'):
        specdoc = False

        for h1 in art.find_all('h1'):
            if h1.text == "Specificatiedocument":
                specdoc = True

        if specdoc == True:
            for a in art.find_all('a'):
                lijst.append(a['href'])
        print('url', lijst[0])
        write_to_file('./test.txt', str(lijst[0]))
        write_to_file('./test.txt', '\n')
        return lijst


def getKlassen(link, driver):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")

    entiteiten = False
    datatypes = False
    klassen = {}
    typedict = {}

    for d in soup.find_all('div', attrs={"class": "region region--no-space-top"}):

        for h2 in d.find_all('h2'):
            if h2.text == "Entiteiten":
                entiteiten = True
        if entiteiten:
            attributen = []
            datatypes = False
            for h3 in d.find_all('h3'):
                for code in d.find_all('code'):
                    for a in code.find_all('a'):
                        attributen.append(a.text[29:])
                klassen[h3.text] = attributen

        for h2 in d.find_all('h2'):
            if h2.text == "Datatypes":
                entiteiten = False
                datatypes = True
        if datatypes:
            attributen = []
            for h3 in d.find_all('h3'):
                for code in d.find_all('code'):
                    for a in code.find_all('a'):
                        attributen.append(a.text)
                typedict[h3.text] = attributen

    stanDict = {}
    stanDict["Entiteiten"] = klassen
    stanDict["Datatypes"] = typedict
    return stanDict


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


def scrape():
    driver = webdriver.Chrome()
    links = getLinks(driver)

    linklijst = []
    for link in links.values():
        for l in getStandaard(link, driver):
            linklijst.append(l)

    resultaat = {}
    for link in linklijst:
        resultaat[link] = getKlassen(link, driver)

    databasefile = "./standaarddb.json"  # os.getcwd()+"\\
    with open(databasefile, "w") as f:
        json.dump(resultaat, f)
    return databasefile


def opzoeken(term):
    resultaten = {}
    f = open(databasefile, "r")
    standaarden = json.loads(f.read())
    for s in standaarden:
        matches = []
        gevonden = False
        for ed in standaarden[s]:
            for klasse in standaarden[s][ed]:
                if term in klasse.lower():
                    matches.append("Klassen:")
                    matches.append(klasse)
                    gevonden = True
                else:
                    for attribuut in standaarden[s][ed][klasse]:
                        if term in attribuut.lower():
                            matches.append("Attibuten:")
                            matches.append(attribuut)
                            gevonden = True
        if gevonden:
            resultaten[s] = matches

    return resultaten


def main():
    inp = input("Wat wil je opzoeken? ")
    zoekresultaten = opzoeken(inp.lower())

    print("")
    for standaard in zoekresultaten.keys():
        print(standaard)
        for klasse in zoekresultaten[standaard]:
            print(klasse)
        print("\n")
    print("##############################################################################\n")


create_empty_file('./test.txt')
#scrape()

driver = webdriver.Chrome()
links = getLinks(driver)
