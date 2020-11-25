from SearchResultsParser.abstract_parser import AbstractResultParser
from SearchResultsParser.urlsdto import UrlsDTO


class SearchFacade:
    def __init__(self, searchers: AbstractResultParser = [], filter=None):
        self.searchers = searchers
        self.filter = filter

    def search_operation(self, query: str, numresults: int) -> UrlsDTO:
        pause = 10
        results: UrlsDTO = UrlsDTO()
        numsearchers = len(self.searchers)
        for i in range(numsearchers):
            results = results + self.searchers[i].search(query, "co.in", numresults, numresults, pause)
        if self.filter is not None:
            results = self.filter.filtering(results)
        return results
