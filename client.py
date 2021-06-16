#! /usr/bin/python3.8
import json
import logging
import click
from search_results_parser.search_facade import SearchFacade
from search_results_parser.abstract_parser import AbstractResultParser
from search_results_parser.google_parser import GoogleParser
from search_results_parser.rambler_parser import RamblerParser
from search_results_parser.yandex_parser import YandexParser
from search_results_parser.filter.filter_urlsdto import FilterUrlsDTO
from search_results_parser.filter.basic_filter import BasicFilter
from search_results_parser.filter.replays_decorator import ReplaysFilter
from search_results_parser.filter.officalsite_decorator import OfficalSiteFilter
from sentiment_analyzer.analyzer import SentimentAnalyzer
from mongodb.config import DevelopingConfig
from mongodb.models import Page
from grabber.grabber import Grabber
from errors import *

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.NOTSET,
        filename="crawler_logs.log",
        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        datefmt='%H:%M:%S',
    )

    if not check_network():
        print("Internet off")
        exit(1)
    print("Internet on")
    db_con = DevelopingConfig('crawlerdb', 'root', 'root', 27017)
    if not db_con.check_connection():
        print("Database not connected")
        exit(1)
    print("Database connected successfully")
    if not check_tor_network():
        print("Tor network off")
        exit(1)
    print("Tor network on")

    name_company = input('Enter your company name:')
    link_official_company = input('Enter the link to the official website of the company:')
    num_results = input('Enter the number of search results:')
    choose_searches = input("Select search  engines,"
                            " separated by space:\n1. Google \n2. Yandex\n3. Rambler\n")
    deep = int(input('Введите глубину поиска:'))

    check_name_company(name_company)
    check_official_link(link_official_company)
    check_num_results(num_results)
    check_choose_searches(choose_searches)
    check_query_patterns('query_patterns.json')
    check_deep(deep)

    num_results = int(num_results)
    choose_searches = choose_searches.split(' ')

    searchers: AbstractResultParser = []
    for i in choose_searches:
        if i == "1":
            searchers.append(GoogleParser())
        elif i == "2":
            searchers.append(YandexParser())
        elif i == "3":
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
    for query in query_patterns['queries']:
        query_list.append(query.format(name_company))

    urls_filter: FilterUrlsDTO = BasicFilter()
    urls_filter = ReplaysFilter(urls_filter)
    urls_filter = OfficalSiteFilter(urls_filter, link_official_company)
    print('Link filters installed:' + urls_filter.get_description())
    logging.info('Link filters installed:' + urls_filter.get_description())

    sf = SearchFacade(searchers, urls_filter)
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
            except Exception as exception:
                logging.error(f"\nCan't connection to page. {link}:{str(exception)}")
            else:
                pages.append(Page(title=link, content=now_text))
    print('End of scraping pages')
    logging.info('End of scraping pages')

    grabber.off_tor()

    db_con.connect()
    with click.progressbar(pages, label="Saving to database") as bar:
        for page in bar:
            logging.info(f"Page saved {page.title}")
            try:
                page.save()
            except Exception as exception:
                logging.error(f'Failed to connect to database:{exception}')
                raise Exception("Failed to connect to database")

    print('Saving data was successful')
    logging.info('Saving data was successful')
    db_con.disconnect()

    analyzer = SentimentAnalyzer()
    analyzer.connect_to_db('crawlerdb', 'root', 'root', 27017)
    analyzer.analyze()
