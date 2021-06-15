import logging
from search_results_parser.abstract_parser import AbstractResultParser
from search_results_parser.urlsdto import UrlsDTO
from search_results_parser.filter.filter_urlsdto import FilterUrlsDTO


class SearchFacade:
    '''Class for simple work with search engines'''

    def __init__(self, searchers: AbstractResultParser = None, urls_filter: FilterUrlsDTO = None) -> None:
        self.searchers: AbstractResultParser = searchers
        self.filter: FilterUrlsDTO = urls_filter

    def search_operation(self, queries: [str], num_results: int) -> UrlsDTO:
        ''':return urls from searches results and filtering'''
        pause = 10
        results: UrlsDTO = UrlsDTO()
        num_searchers = len(self.searchers)
        for query in queries:
            for i in range(num_searchers):
                logging.info(f"now query:\"{query} using {self.searchers[i].get_description()}\"")
                results = results + \
                          self.searchers[i].search(query, "co.in", num_results, num_results, pause)

        logging.info(f"Not filtered urls:{results}")
        if self.filter is not None:
            results = self.filter.filtering(results)
            logging.info(f"used filter \"{self.filter.get_description()}\"")
            logging.info(f"Filtered urls:{results}")
        return results
