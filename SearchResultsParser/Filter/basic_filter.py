from abc import ABC, abstractmethod
from SearchResultsParser.urlsdto import UrlsDTO
from .filter_urlsdto import FilterUrlsDTO


class BasicFilter(FilterUrlsDTO):
    def __init__(self):
        self._description = "Basic filter"

    def filtering(self, data: UrlsDTO = None) -> UrlsDTO:
        return data
