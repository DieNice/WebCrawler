from abc import abstractclassmethod
from SearchResultsParser.urlsdto import UrlsDTO
from .filter_urlsdto import FilterUrlsDTO


class FilterDecorator(FilterUrlsDTO):
    '''class decorator for filtering'''
    @abstractclassmethod
    def filtering(cls, data: UrlsDTO = None) -> UrlsDTO:
        pass
