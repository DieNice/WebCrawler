import logging

from SearchResultsParser.abstract_parser import AbstractResultParser
from SearchResultsParser.urlsdto import UrlsDTO
from SearchResultsParser.Filter.filter_urlsdto import FilterUrlsDTO
import click


class SearchFacade:
    def __init__(self, searchers: AbstractResultParser = [], filter: FilterUrlsDTO = None):
        self.searchers: AbstractResultParser = searchers
        self.filter: FilterUrlsDTO = filter

    def search_operation(self, queries: [str], num_results: int) -> UrlsDTO:
        ''':return urls from searches results and filtering'''
        pause = 10
        results: UrlsDTO = UrlsDTO()
        num_searchers = len(self.searchers)
        for query in queries:
            for i in range(num_searchers):
                logging.info(f"now query:\"{query} using {self.searchers[i].get_description()}\"")
                results = results + self.searchers[i].search(query, "co.in", num_results, num_results, pause)

        logging.info(f"Not filtered urls:{results}")
        if self.filter is not None:
            results = self.filter.filtering(results)
            logging.info(f"used filter \"{self.filter.getDescription()}\"")
            logging.info(f"Filtered urls:{results}")
        return results
