from .filter_urlsdto import FilterUrlsDTO
from abc import ABC, abstractclassmethod
from SearchResultsParser.urlsdto import UrlsDTO


class FilterDecorator(FilterUrlsDTO):
    @abstractclassmethod
    def filtering(self, data: UrlsDTO = None) -> UrlsDTO:
        pass
