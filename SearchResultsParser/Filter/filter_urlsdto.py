from abc import ABC, abstractmethod
from SearchResultsParser.urlsdto import UrlsDTO


class FilterUrlsDTO(ABC):
    '''Filtering class'''
    def __init__(self):
        super.__init__()
        self._description = "Unknown filter"

    def getDescription(self):
        ''':return description of all filters'''
        return self._description

    @abstractmethod
    def filtering(self, data: UrlsDTO = None) -> UrlsDTO:
        ''':return filtered UrlsDTO'''
        pass
