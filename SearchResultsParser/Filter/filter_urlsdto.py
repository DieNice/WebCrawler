from abc import ABC, abstractmethod
from SearchResultsParser.urlsdto import UrlsDTO


class FilterUrlsDTO(ABC):
    '''Filtering class'''
    def __init__(self) -> None:
        self._description = "Unknown filter"

    def get_description(self) -> str:
        ''':return description of all filters'''
        return self._description

    @abstractmethod
    def filtering(self, data: UrlsDTO = None) -> UrlsDTO:
        ''':return filtered UrlsDTO'''
