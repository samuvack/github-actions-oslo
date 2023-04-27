from pytz import timezone
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import os
from pprintpp import pprint
from datetime import datetime, timedelta

"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 800))
display.start()


# Check if the current version of chromedriver exists
chromedriver_autoinstaller.install()
# and if it doesn't exist, download it automatically,
# then add chromedriver to path

chrome_options = webdriver.ChromeOptions()
# Add your options as needed
options = [
    # Define window size here
    "--window-size=1200,1200",
    "--ignore-certificate-errors"

    # "--headless",
    # "--disable-gpu",
    # "--window-size=1920,1200",
    # "--ignore-certificate-errors",
    # "--disable-extensions",
    # "--no-sandbox",
    # "--disable-dev-shm-usage",
    # '--remote-debugging-port=9222'
]

for option in options:
    chrome_options.add_argument(option)


driver = webdriver.Chrome(options=chrome_options)
"""



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

# haal data uit AP


def getData(link, driver):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")

    entiteiten = False
    datatypes = False
    klassen = []
    typedict = []

    for d in soup.find_all('div', attrs={"class": "region region--no-space-top"}):
        # entiteiten ophalen
        for h2 in d.find_all('h2'):
            if h2.text == "Entiteiten":
                entiteiten = True
        if entiteiten:
            datatypes = False
            for h3 in d.find_all('h3'):  # hier zit je in de box van een klasse
                for a in h3.find_all('a'):  # link van de klasse zelf in een dict
                    linkdict = {'link': a['href']}
                # hier zit je in de box met de informatie van de klasse zelf
                for dl in d.find_all('dl'):
                    beschr = False  # steek beschrijving in een dict
                    for dt in dl.find_all(['dt', 'dd']):
                        if beschr:
                            beschrijving = {'beschrijving': dt.text}
                            beschr = False
                        if dt.text == "Beschrijving":
                            beschr = True

                # enkel de beschrijving wordt opgeslagen, de rest kan maar lijkt nutteloos

                # attributen ophalen
                attributen = {}
                for tr in d.find_all('tr', attrs={"typeof": "rdfs:Property"}):
                    lijst = []
                    for td in tr.find_all('td'):
                        geenLink = True
                        for a in td.find_all('a'):
                            attrlink = {}
                            if a.text[5:10] == "     ":
                                attrlink[a.text[29:]] = a['href']
                            else:
                                attrlink[a.text] = a['href']
                            lijst.append(attrlink)
                            geenLink = False
                        if geenLink:
                            lijst.append(td.text)

                    attributen['attributen'] = lijst
                if attributen == {}:
                    attributen['attributen'] = [{'bla': 'bla'}, {
                        'bla': 'bla'}, 'bla', 'bla', 'bla', 'bla']
                klasse = [linkdict, beschrijving, attributen]
                klassen.append({h3.text: klasse})

        # datatypes ophalen
        for h2 in d.find_all('h2'):
            if h2.text == "Datatypes":
                datatypes = True
        if datatypes:
            entiteiten = False
            for h3 in d.find_all('h3'):  # hier zit je in de box van een datatype
                for a in h3.find_all('a'):  # link van het datatype zelf in een dict
                    linkdict = {'link': a['href']}
                # hier zit je in de box met de informatie van het datatype zelf
                for dl in d.find_all('dl'):
                    beschr = False  # steek beschrijving in een dict
                    for dt in dl.find_all(['dt', 'dd']):
                        if beschr:
                            beschrijving = {'beschrijving': dt.text}
                            beschr = False
                        if dt.text == "Beschrijving":
                            beschr = True

                # enkel de beschrijving wordt opgeslagen, de rest kan maar lijkt nutteloos

                # attributen ophalen
                attributen = {}
                for tr in d.find_all('tr', attrs={"typeof": "rdfs:Property"}):
                    lijst = []
                    for td in tr.find_all('td'):
                        geenLink = True
                        for a in td.find_all('a'):
                            attrlink = {}
                            if a.text[5:10] == "     ":
                                attrlink[a.text[29:]] = a['href']
                            else:
                                attrlink[a.text] = a['href']
                            lijst.append(attrlink)
                            geenLink = False
                        if geenLink:
                            lijst.append(td.text)

                    attributen['attributen'] = lijst
                if attributen == {}:
                    attributen['attributen'] = [{'bla': 'bla'}, {
                        'bla': 'bla'}, 'bla', 'bla', 'bla', 'bla']
                datatype = [linkdict, beschrijving, attributen]
                typedict.append({h3.text: datatype})

    stanDict = {}
    stanDict["Entiteiten"] = klassen
    stanDict["Datatypes"] = typedict
    return stanDict

# analyseer het AP
geenfixme = 0
geenbeschrijving = 0
geentype = 0
geenkardinaliteit = 0
geendefenitie = 0
text = ""


def analyse(data, geenfixme, geenbeschrijving, geentype, geenkardinaliteit, geendefenitie):
    resultaat = ""
    for soort in data:
        for entiteit in data[soort]:

            # link van klasse zelf checken
            if "fixme" in list(entiteit.values())[0][0]['link']:
                geenfixme = geenfixme + 1
                resultaat += "```diff \ - fixme gevonden in de link van klasse \"{}\" ``` <br>".format(
                    list(entiteit.keys())[0])

            # beschrijving van de klasse zelf checken
            if list(entiteit.values())[0][1]['beschrijving'] == "":
                resultaat += "```diff \ - Geen beschrijving gevonden bij klasse \"{}\" ``` <br>".format(
                    list(entiteit.keys())[0])

            # attributen hier overlopen
            attribuut = list(list(list(entiteit.values())[
                             0][2].values())[0][0].keys())[0]
            attributen = list(list(entiteit.values())[0][2].values())[0]

            cel = attributen[0]
            if "fixme" in cel[list(cel.keys())[0]]:
                geenfixme = geenfixme + 1
                resultaat += "```diff \ - fixme gevonden in attribuut \"{}\" van klasse \"{}\" ``` <br>".format(
                    attribuut, list(entiteit.keys())[0])
            cel = attributen[1]
            try:
                if "fixme" in cel[list(cel.keys())[0]]:
                    geenfixme = geenfixme + 1
                    resultaat += "```diff \ - fixme gevonden in attribuut \"{}\" van klasse \"{}\"``` <br>".format(
                        attribuut, list(entiteit.keys())[0])
            except:
                geentype = geentype + 1
                resultaat += "```diff \ - Geen verwacht type gevonden bij attribuut \"{}\" van klasse \"{}\" ``` <br>".format(
                    attribuut, list(entiteit.keys())[0])
            cel = attributen[2]
            if cel == "":
                geenkardinaliteit = geenkardinaliteit + 1
                resultaat += "```diff \ - Kardinaliteit ontbreekt in attribuut \"{}\" van klasse \"{}\"``` <br>".format(
                    attribuut, list(entiteit.keys())[0])
            cel = attributen[3]
            if cel == "":
                geendefenitie = geendefenitie + 1
                resultaat += "```diff \ - Definitie ontbreekt in attribuut \"{}\" van klasse \"{}\"``` <br>".format(
                    attribuut, list(entiteit.keys())[0])

    if resultaat == "":
        resultaat += "```diff \ + Alles is in orde!```"

    return resultaat, geenfixme, geenbeschrijving, geentype, geenkardinaliteit, geendefenitie


driver = webdriver.Chrome()

links = ['https://data.vlaanderen.be/doc/applicatieprofiel/bedrijventerrein/', 'https://data.vlaanderen.be/doc/applicatieprofiel/besluit-publicatie/', 'https://data.vlaanderen.be/doc/applicatieprofiel/besluitvorming', 'https://data.vlaanderen.be/doc/applicatieprofiel/contactvoorkeuren/', 'https://data.vlaanderen.be/doc/applicatieprofiel/cultureel-erfgoed-event', 'https://data.vlaanderen.be/doc/applicatieprofiel/cultureel-erfgoed-object', 'https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL/erkendestandaard/2021-12-02', 'https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL', 'https://data.vlaanderen.be/doc/applicatieprofiel/dienst-transactiemodel/', 'https://data.vlaanderen.be/doc/applicatieprofiel/dossier/', 'https://data.vlaanderen.be/doc/applicatieprofiel/generieke-terugmeldfaciliteit/', 'https://data.vlaanderen.be/doc/applicatieprofiel/issue-tracking-voor-burgers-en-organisaties/', 'https://data.vlaanderen.be/doc/applicatieprofiel/ldes', 'https://data.vlaanderen.be/doc/applicatieprofiel/mandatendatabank/', 'https://data.vlaanderen.be/doc/applicatieprofiel/metadata-dcat/', 'https://data.vlaanderen.be/doc/applicatieprofiel/mobiliteit/dienstregeling-en-planning/stopplaatsen/', 'https://data.vlaanderen.be/doc/applicatieprofiel/mobiliteit/dienstregeling-en-planning/tijdstabellen/', 'https://data.vlaanderen.be/doc/applicatieprofiel/mobiliteit/dienstregeling-en-planning/voertuigplanning/', 'https://data.vlaanderen.be/doc/applicatieprofiel/mobiliteit-trips-en-aanbod', 'https://data.vlaanderen.be/doc/applicatieprofiel/notificatie-basis/', 'https://data.vlaanderen.be/doc/applicatieprofiel/openbaar-domein/', 'https://data.vlaanderen.be/doc/applicatieprofiel/perceel/', 'https://data.vlaanderen.be/doc/applicatieprofiel/logies-basis/', 'https://data.vlaanderen.be/doc/applicatieprofiel/mobiliteit/vervoersknooppunten', 'https://data.vlaanderen.be/doc/applicatieprofiel/vlaamse-codex/', 'https://data.vlaanderen.be/doc/applicatieprofiel/begraafplaatsenbeheer/', 'https://data.vlaanderen.be/doc/applicatieprofiel/begroeid-voorkomen/', 'https://data.vlaanderen.be/doc/applicatieprofiel/infrastructuurelementen/', 'https://data.vlaanderen.be/doc/applicatieprofiel/onbegroeid-voorkomen/', 'https://data.vlaanderen.be/doc/applicatieprofiel/terreindelen/', 'https://data.vlaanderen.be/doc/applicatieprofiel/vegetatie-elementen/', 'https://data.vlaanderen.be/doc/applicatieprofiel/watervoorkomen/', 'https://data.vlaanderen.be/doc/applicatieprofiel/waterdelen/', 'https://data.vlaanderen.be/doc/applicatieprofiel/begraafplaatsen', 'https://data.vlaanderen.be/doc/applicatieprofiel/begraafplaatsenbeheer', 'https://data.vlaanderen.be/doc/applicatieprofiel/begroeid-voorkomen', 'https://data.vlaanderen.be/doc/applicatieprofiel/gebieden', 'https://data.vlaanderen.be/doc/applicatieprofiel/infrastructuurelementen', 'https://data.vlaanderen.be/doc/applicatieprofiel/onbegroeid-voorkomen', 'https://data.vlaanderen.be/doc/applicatieprofiel/terreindelen',
         'https://data.vlaanderen.be/doc/applicatieprofiel/vegetatie-elementen', 'https://data.vlaanderen.be/doc/applicatieprofiel/waterdelen', 'https://data.vlaanderen.be/doc/applicatieprofiel/watervoorkomen', 'https://data.vlaanderen.be/doc/applicatieprofiel/openbaar-domein', 'https://data.vlaanderen.be/doc/applicatieprofiel/openbaar-domein', 'https://data.vlaanderen.be/doc/applicatieprofiel/gebieden', 'https://data.vlaanderen.be/doc/applicatieprofiel/infrastructuurelementen', 'https://data.vlaanderen.be/doc/applicatieprofiel/vegetatie-elementen', 'https://data.vlaanderen.be/doc/applicatieprofiel/terreindelen', 'https://data.vlaanderen.be/doc/applicatieprofiel/begroeid-voorkomen', 'https://data.vlaanderen.be/doc/applicatieprofiel/onbegroeid-voorkomen', 'https://data.vlaanderen.be/doc/applicatieprofiel/waterdelen', 'https://data.vlaanderen.be/doc/applicatieprofiel/watervoorkomen', 'https://data.vlaanderen.be/doc/applicatieprofiel/begraafplaatsen', 'https://data.vlaanderen.be/doc/applicatieprofiel/begraafplaatsenbeheer', 'https://data.vlaanderen.be/doc/applicatieprofiel/bedrijventerrein/', 'https://data.vlaanderen.be/doc/applicatieprofiel/dossier/', 'https://data.vlaanderen.be/doc/applicatieprofiel/adresregister/', 'https://data.vlaanderen.be/doc/applicatieprofiel/besluit-mobiliteit/', 'https://data.vlaanderen.be/doc/applicatieprofiel/subsidieregister/', 'https://data.vlaanderen.be/doc/applicatieprofiel/bestuurlijk-sanctieregister', 'https://data.vlaanderen.be/doc/applicatieprofiel/bodem-en-ondergrond/bodem-en-ondergrond/kandidaatstandaard/2022-04-28', 'https://data.vlaanderen.be/doc/applicatieprofiel/dienstencataloog/', 'https://data.vlaanderen.be/doc/applicatieprofiel/cultuurparticipatie', 'https://data.vlaanderen.be/doc/applicatieprofiel/FeitelijkeVerenigingen/', 'https://data.vlaanderen.be/doc/applicatieprofiel/financiele-data', 'https://test.data.vlaanderen.be/doc/applicatieprofiel/gebouwenregister/', 'https://data.vlaanderen.be/doc/applicatieprofiel/inname-openbaar-domein/', 'https://data.vlaanderen.be/doc/applicatieprofiel/loongegevens', 'https://data.vlaanderen.be/doc/applicatieprofiel/observaties-en-metingen/kandidaatstandaard/2022-04-28', 'https://data.vlaanderen.be/doc/applicatieprofiel/organisatie-basis/', 'https://data.vlaanderen.be/doc/applicatieprofiel/persoon-basis/', 'https://data.vlaanderen.be/doc/applicatieprofiel/sensoren-en-bemonstering/kandidaatstandaard/2022-04-28', 'https://data.vlaanderen.be/doc/applicatieprofiel/verkeersborden/', 'https://data.vlaanderen.be/doc/applicatieprofiel/wegenregister/', 'https://data.vlaanderen.be/doc/applicatieprofiel/cultureel-erfgoed-object', 'https://data.vlaanderen.be/doc/applicatieprofiel/cultureel-erfgoed-event', 'https://data.vlaanderen.be/doc/applicatieprofiel/cultuur-en-jeugdinfrastructuur', 'https://data.vlaanderen.be/doc/applicatieprofiel/waterkwaliteit', 'https://data.vlaanderen.be/doc/applicatieprofiel/statistiek', 'https://data.vlaanderen.be/doc/applicatieprofiel/datakwaliteit']
create_empty_file("README.md")
write_to_file('README.md', "## OSLO standarden en applicatie profielen HTML validatie")
write_to_file('README.md', '\n')
write_to_file('README.md', '<br />')


# using now() to get current time
current_time = datetime.now() + timedelta(hours=1)

# Printing value of now.
print(current_time)

write_to_file(
    'README.md', """```diff
    ! Dit document is automatisch gevalideerd op : """ + str(current_time) + """```""")
write_to_file('README.md', '<br />')

for link in links:
    data = getData(link, driver)
    resultaat = analyse(data, geenfixme, geenbeschrijving,
                        geentype, geenkardinaliteit, geendefenitie)[0]
    if (resultaat == """Alles is in orde!"""):
        print(link, "<br />")
        print(resultaat, "<br /><br />")
        write_to_file('README.md', '<br />')
        write_to_file('README.md', "["+link+"]("+link+")")
        write_to_file('README.md', '<br />')
        print(resultaat)
        write_to_file('README.md', resultaat)
        
        write_to_file('README.md', '<br />')
    else:
        print(link, "<br />")
        print(resultaat, "<br /><br />")
        write_to_file('README.md', '<br />')
        write_to_file('README.md', "["+link+"]("+link+")")
        write_to_file('README.md', '<br />')
        print(resultaat)
        write_to_file('README.md', resultaat)
        write_to_file('README.md', '<br />')
    
