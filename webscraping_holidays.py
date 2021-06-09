import requests
from bs4 import BeautifulSoup
import holidays
from datetime import date
import csv

def webscrape():
    """
    Web scraping 3 character ISO and country name from holidays
    documentation site

    :return countries:  {3 character ISO: [Country, states]}
    :type countries: dict

    """
    url = 'https://pypi.org/project/holidays/'
    countries = {}
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    iso_table = soup.find('table')

    for country in iso_table.find_all('tbody'):
        rows = country.find_all('tr')
        for row in rows:
            c = row.find_all('td')
            if '/' not in c[1].text:
                continue
            else:
                if len(c[1].text.split('/')[1]) == 3:
                    prov = ''
                    if c[2].text != None:
                        prov = c[2].text.strip()
                        if '\n' in prov:
                            prov = prov.replace('\n', ' ')
                        if ' (default)' in prov:
                            prov = prov.replace(' (default)', '')
                        if 'prov = ' in prov:
                            prov = prov.replace('prov = ', '')
                        if 'state = ' in prov:
                            prov = prov.replace('state = ', '')
                        if prov == '' or prov == 'None':
                            prov = None

                    countries[c[1].text.split('/')[1]] = [c[0].text, prov]
    return countries

def getHolidays(countries):
    """
    Get holiday dates for years in range 2016-2022 for
    supported countries

    :param countries:
    :type countries: dict
    :return country_holidays:
    :type country_holidays: dict

    """
    country_holidays = {}

    for c in countries.keys():
        country_holidays[c] = {}
        for year in range(2016, 2022+1):
            country_holidays[c][year] = holidays.CountryHoliday(countries[c][0], years=year)


    return country_holidays

def writeHolidays(countries, country_holidays):
    """
    Writes countries and their holidays to csv file holidays.csv

    :param countries, country_holidays:
    :type countries, country_holidays: dict

    """

    with open('holidays.csv', mode='w', newline='') as csv_file:
        headers = ['ISO', 'Country', 'States', '2016', '2017', '2018', '2019', '2020', '2021', '2022']
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()

        for c in country_holidays:
            holidays16 = [k for k in country_holidays[c][2016]]
            holidays17 = [k for k in country_holidays[c][2017]]
            holidays18 = [k for k in country_holidays[c][2018]]
            holidays19 = [k for k in country_holidays[c][2019]]
            holidays20 = [k for k in country_holidays[c][2020]]
            holidays21 = [k for k in country_holidays[c][2021]]
            holidays22 = [k for k in country_holidays[c][2022]]
            writer.writerow({'ISO': c, 'Country': countries[c][0], 'States': countries[c][1], '2016': str(holidays16), '2017': str(holidays17),
            '2018': str(holidays18), '2019': str(holidays19), '2020': str(holidays20), '2021': str(holidays21), '2022': str(holidays22)})

def summary(country_holidays):
    """
    Summary of number of holidays in each supported
    country for each year in the range 2016-2022

    :param country_holidays:
    :type country_holidays: dict
    :return nbr_holidays: {ISO: [2016, ..., 2022]
    :type nbr_holidays: dict

    """

    nbr_holidays = {}
    for c in country_holidays:

        if c != 'SWE' or c != 'NOR':
            nbr_holidays[c] = [len(country_holidays[c][2016]), len(country_holidays[c][2017]), len(country_holidays[c][2018]), len(country_holidays[c][2019]), len(country_holidays[c][2020]), len(country_holidays[c][2021]), len(country_holidays[c][2022])]

        # Remove regular Sundays from holidays count for Sweden and Norway
        if c == 'SWE' or c == 'NOR':
            nbr_holidays[c] = []
            for y in range(2016, 2022+1):
                nbr_holidays_y = len(country_holidays[c][y])
                for dt in country_holidays[c][y]:
                    date_ = dt.strftime("%Y-%m-%d")
                    if country_holidays[c][y].get(date_) == 'Söndag' or country_holidays[c][y].get(date_) == 'Søndag':
                        nbr_holidays_y -= 1
                nbr_holidays[c].append(nbr_holidays_y)

    return nbr_holidays

def writeSummary(nbr_holidays):
    """
    Writes summary of number of holidays to csv file nbr_holidays.csv

    :param nbr_holidays:
    :tye nbr_holidays: dict

    """

    with open('nbr_holidays.csv', mode='w', newline='') as csv_file:
        headers = ['ISO', '2016', '2017', '2018', '2019', '2020', '2021', '2022']
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()

        for c in nbr_holidays:
            writer.writerow({'ISO': c, '2016': nbr_holidays[c][0], '2017': nbr_holidays[c][1], '2018': nbr_holidays[c][2], '2019': nbr_holidays[c][3], '2020': nbr_holidays[c][4], '2021': nbr_holidays[c][5], '2022': nbr_holidays[c][6]})



def run():
    countries = webscrape()
    country_holidays = getHolidays(countries)
    writeHolidays(countries, country_holidays)
    nbr_holidays = summary(country_holidays)
    writeSummary(nbr_holidays)
 

run()
