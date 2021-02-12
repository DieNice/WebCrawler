from abc import ABC, abstractmethod
from SearchResultsParser.urlsdto import UrlsDTO


class FilterUrlsDTO(ABC):
    def __init__(self):
        super.__init__()
        self._description = "Unknown filter"

    def getDescription(self):
        return self._description

    @abstractmethod
    def filtering(self, data: UrlsDTO = None) -> UrlsDTO:
        pass
