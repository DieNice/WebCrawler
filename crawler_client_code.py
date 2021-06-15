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
import logging
import validators
import json
import click
import logging


def check_name_company(name_company: str) -> bool:
    '''check function of namecompany'''
    if len(name_company) == 0:
        raise Exception('Company name cannot be empty')
    if name_company.isdigit():
        raise Exception('Company name cannot contain only numbers')
    if validators.url(name_company):
        raise Exception('Comapany name cannot be URL')
    return True


def check_official_link(official_link: str) -> bool:
    '''check function of offical link company'''
    if not validators.url(official_link):
        raise Exception('Incorrect official site URL')
    return True


def check_num_results(num_results: int) -> bool:
    '''check function num results'''
    if not str(num_results).isdigit():
        raise Exception('The number of search results is incorrect')
    if num_results < 0:
        raise Exception('The number of search result can\'t be than less 0')
    return True


def check_choose_searches(choose_searches: str) -> bool:
    '''check function choose searches'''
    correct_numbers = ['1', '2', '3']
    choose_searches = choose_searches.split(' ')
    for choose in choose_searches:
        if not choose.isdigit():
            raise Exception(f"{choose} is not number of search engine")
        if not choose in correct_numbers:
            raise Exception(f"{choose} is not exists number search engine")
    return True


def check_query_patterns(filepath: str) -> bool:
    '''check function query patterns'''
    with open(filepath, 'r') as f:
        try:
            query_patterns = json.load(f)
        except json.decoder.JSONDecodeError:
            raise Exception("Invalid JSON")
        else:
            if len(query_patterns) > 1:
                raise Exception('The number of keys in the configuration file cannot be more than 1 key \"queries\"')
            if len(query_patterns) < 1:
                raise Exception('No fields in configuration query patterns')
        queries: str = query_patterns['queries']
        for query in queries:
            if query.find('{}') < 0:
                raise Exception(f"Query \"{query}\" missing brackets " + "{}")
    return True


def check_deep(deep: int) -> bool:
    '''check function deep'''
    if not str(deep).isdigit():
        raise Exception('The deep is incorrect')
    if deep < 0:
        raise Exception('The deep can\'t be than less or equal 0')
    return True


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.NOTSET,
        filename="crawler_logs.log",
        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        datefmt='%H:%M:%S',
    )
    name_company = input('Enter your company name:')
    link_official_company = input('Enter the link to the official website of the company:')
    num_results = int(input('Enter the number of search results:'))
    choose_searches = input("Select search  engines, separated by space:\n1. Google \n2. Yandex\n3. Rambler\n")
    deep = int(input('Введите глубину поиска:'))

    check_name_company(name_company)
    check_official_link(link_official_company)
    check_num_results(num_results)
    check_choose_searches(choose_searches)
    check_query_patterns('query_patterns.json')
    check_deep(deep)

    choose_searches = choose_searches.split(' ')

    searchers: AbstractResultParser = []
    for i in choose_searches:
        if "1" == i:
            searchers.append(GoogleParser())
        elif "2" == i:
            searchers.append(YandexParser())
        elif "3" == i:
            searchers.append(RamblerParser())
    print('Search Engines Selected\n')
    logging.info('Search Engines Selected')

    try:
        with open('query_patterns.json', 'r') as f:
            query_patterns = json.load(f)
    except FileNotFoundError:
        print('Request config file not found!')
        logging.error('Request config file not found!')
    else:
        print('Configuration file read successfully!')
        logging.info('Configuration file read successfully!')
    query_list = []
    for i in query_patterns['queries']:
        query_list.append(i.format(name_company))

    filter: FilterUrlsDTO = BasicFilter()
    filter = ReplaysFilter(filter)
    filter = OfficalSiteFilter(filter, link_official_company)
    print('Link filters installed:' + filter.getDescription())
    logging.info('Link filters installed:' + filter.getDescription())

    sf = SearchFacade(searchers, filter)
    print('Start parsing search results:')
    logging.info("Start parsing search results:")
    start_links = sf.search_operation(query_list, num_results)
    print('End of parsing search results')
    logging.info("End of parsing search results")

    pages: [Page] = []
    print('Start scraping pages:')
    logging.info('Start scraping pages:')

    grabber = Grabber()
    with click.progressbar(start_links) as bar:
        for link in bar:
            try:
                now_text = grabber.get_text(link)
            except Exception as e:
                print(f"\nCan't connection to page. {link}:{str(e)}")
                logging.error(f"\nCan't connection to page. {link}:{str(e)}")
            else:
                pages.append(Page(title=link, content=now_text))
    print('End of scraping pages')
    logging.info('End of scraping pages')

    grabber.off_tor()
    print('Database connection')
    logging.info('Database connection')
    try:
        connect = DevelopingConfig('crawlerdb', 'root', 'root', 27017)
    except Exception as ex:
        print('Failed to connect to database:', ex)
        logging.error(f'Failed to connect to database:{ex}')
    print('Database connection successful!\nSaving the results to the database\n')
    logging.info('Database connection successful!\nSaving the results to the database')

    with click.progressbar(pages, label="Saving to database") as bar:
        for page in bar:
            logging.info(f"Page saved {page.title}")
            page.save()
    print('Saving data was successful')
    logging.info('Saving data was successful')
