from search_results_parser.urlsdto import UrlsDTO
from .filter_urlsdto import FilterUrlsDTO


class BasicFilter(FilterUrlsDTO):
    '''Basic empty filter clas'''

    def __init__(self) -> None:
        self._description = "Basic filter"

    def filtering(self, data: UrlsDTO = None) -> UrlsDTO:
        return data
