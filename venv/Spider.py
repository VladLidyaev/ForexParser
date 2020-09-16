import requests
from bs4 import BeautifulSoup
import csv

HEADERS = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0','Accept': '*/*'}

FILE = 'News.csv'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def save_files(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['INFO'])
        for item in items:
            writer.writerow([item['info']])

def get_url():
    Links = []
    month : int
    for year in range(2007, 2021):
        for month in range(1, 13):
            if month in [1, 3, 5, 7, 8, 10, 12]:
                for day in range(1, 32):

                    if int(month) < 10:
                        strmonth = '0' + str(month)
                    else:
                        strmonth = str(month)

                    if int(day) < 10:
                        strday = '0' + str(day)
                    else:
                        strday = str(day)

                    stryear = str(year)

                    url = 'https://www.teletrade.ru/analytics/economical_calendar/date-' + strday + '-' + strmonth + '-' + stryear

                    Links.append({
                        'link': url
                    })

                    day += 1

            if month in [4, 6, 9, 11]:
                for day in range(1, 31):

                    if int(month) < 10:
                        strmonth = '0' + str(month)
                    else:
                        strmonth = str(month)

                    if int(day) < 10:
                        strday = '0' + str(day)
                    else:
                        strday = str(day)

                    stryear = str(year)

                    url = 'https://www.teletrade.ru/analytics/economical_calendar/date-' + strday + '-' + strmonth + '-' + stryear
                    Links.append({
                        'link': url
                    })
                    day += 1

            if month == 2:
                if year in [2008, 2012, 2016, 2020]:
                    for day in range(1, 30):
                        if int(month) < 10:
                            strmonth = '0' + str(month)
                        else:
                            strmonth = str(month)

                        if int(day) < 10:
                            strday = '0' + str(day)
                        else:
                            strday = str(day)

                        stryear = str(year)

                        url = 'https://www.teletrade.ru/analytics/economical_calendar/date-' + strday + '-' + strmonth + '-' + stryear
                        Links.append({
                            'link': url
                        })
                        day += 1
                else:
                    for day in range(1, 29):
                        if int(month) < 10:
                            strmonth = '0' + str(month)
                        else:
                            strmonth = str(month)

                        if int(day) < 10:
                            strday = '0' + str(day)
                        else:
                            strday = str(day)

                        stryear = str(year)

                        url = 'https://www.teletrade.ru/analytics/economical_calendar/date-' + strday + '-' + strmonth + '-' + stryear
                        Links.append({
                            'link': url
                        })
                        day += 1
            month += 1
        year += 1
    return Links

def no_space2(strng):
    return ' '.join(strng.replace('\n', ' ').split())

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(class_='event_value')
    for item in items:
        return (no_space2 (item.text))

def parse():
    LINKS = get_url()
    start = False

    Text = []

    for link in LINKS:
        # print(str(link))
        if '01-03-2007' in str(link):
            start = True
        if start == True:
            words = get_content(get_html(str(link).rpartition("'")[0].rpartition("'")[2]).text)
            words = str(link).rpartition('date-')[2].rpartition("'")[0] + ' ' + str(words)
            Text.append({
                'info': words
            })
            print(words)

    save_files(Text,FILE)

parse()