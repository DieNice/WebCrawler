from SearchResultsParser.search_facade import SearchFacade
from SearchResultsParser.abstract_parser import AbstractResultParser
from SearchResultsParser.google_parser import GoogleParser
from SearchResultsParser.rambler_parser import RamblerParser
from SearchResultsParser.yandex_parser import YandexParser
from SearchResultsParser.Filter.filter_urlsdto import FilterUrlsDTO
from SearchResultsParser.Filter.basic_filter import BasicFilter
from SearchResultsParser.Filter.replays_decorator import ReplaysFilter
from SearchResultsParser.Filter.officalsite_decorator import OfficalSiteFilter

import json

if __name__ == '__main__':
    namecompany = input('Введите название компании:')
    linkofficalcompany = input('Введите ссылку на официальный сайт компании:')
    numresults = int(input('Введите количество результатов поисковой выдачи:'))
    choosesearhes = input("Выберите поисковые системы, через пробел:\n1. Google \n2. Yandex\n3. Rambler\n")
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

    deep = int(input('Введите глубину поиска:'))

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
