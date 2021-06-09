from SearchResultsParser.search_facade import SearchFacade
from SearchResultsParser.abstract_parser import AbstractResultParser
from SearchResultsParser.google_parser import GoogleParser
from SearchResultsParser.rambler_parser import RamblerParser
from SearchResultsParser.yandex_parser import YandexParser
from SearchResultsParser.Filter.filter_urlsdto import FilterUrlsDTO
from SearchResultsParser.Filter.basic_filter import BasicFilter
from SearchResultsParser.Filter.replays_decorator import ReplaysFilter
from SearchResultsParser.Filter.officalsite_decorator import OfficalSiteFilter
from Mongodb.config import DevelopingConfig
from Mongodb.models import Page
from Grabber.grabber import Grabber
from mongoengine import *
import datetime
import json
import click

if __name__ == '__main__':

    # namecompany = input('Введите название компании:')
    # linkofficalcompany = input('Введите ссылку на официальный сайт компании:')
    # numresults = int(input('Введите количество результатов поисковой выдачи:'))
    # choosesearhes = input("Выберите поисковые системы, через пробел:\n1. Google \n2. Yandex\n3. Rambler\n")

    namecompany = "Спортмастер"
    linkofficalcompany = "https://www.sportmaster.ru/?nomobile=1&gclid=CjwKCAjwqvyFBhB7EiwAER786R4mSHPTstQ16BTvx7Mgp9gRGaiqsbf7AZfPDyyT57KYA2RlclH2choCUh8QAvD_BwE"
    numresults = 30
    choosesearhes = '1 2 3'
    choosesearhes = choosesearhes.split(' ')

    searchers: AbstractResultParser = []
    for i in choosesearhes:
        if "1" in choosesearhes:
            searchers.append(GoogleParser())
        elif "2" in choosesearhes:
            searchers.append(YandexParser())
        elif "3" in choosesearhes:
            searchers.append(RamblerParser())
    print('Поисковые системы выбраны\n')

    # deep = int(input('Введите глубину поиска:'))
    deep = 1
    try:
        with open('query_patterns.json', 'r') as f:
            query_patterns = json.load(f)
    except FileNotFoundError:
        print('Файл конфигурации запросов не найден!')
    else:
        print('Файл конфигурации успешно считан!')
    query_list = []
    for i in query_patterns['queries']:
        query_list.append(i.format(namecompany))

    filter: FilterUrlsDTO = BasicFilter()
    filter = ReplaysFilter(filter)
    filter = OfficalSiteFilter(filter, linkofficalcompany)
    print('Фильтры ссылок установлены:' + filter.getDescription())

    sf = SearchFacade(searchers, filter)
    print('Начало парсинга поисковой выдачи:')
    startlinks = sf.search_operation(query_list, numresults)
    print('Конец парсинга поисковой выдачи')

    pages: [Page] = []
    print('Начало скрапинга страниц:')
    grabber = Grabber()
    count = 0
    with click.progressbar(startlinks) as bar:
        for link in bar:
            try:
                textnow = grabber.get_text(link)
            except Exception as e:
                print(f"\nCan't connection to page. Connection timed out {link}:{str(e)}")
            else:
                pages.append(Page(title=link, content=textnow))
    print('Конец скрапинга страниц')

    grabber.off_tor()
    print('Подключение к базе данных')
    try:
        connect = DevelopingConfig('crawlerdb', 'root', 'root', 27017)
    except Exception as ex:
        print('Не удалось подключиться к базе данных:', ex)
    print('Подключение к базе данных успешно!')
    print('Сохранение результатов в базу данных.')

    for page in pages:
        page.save()
    print('Сохранение данных прошло успешно')
