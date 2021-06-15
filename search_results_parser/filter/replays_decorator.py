from search_results_parser.urlsdto import UrlsDTO
from .filter_decorator import FilterDecorator
from .filter_urlsdto import FilterUrlsDTO


class ReplaysFilter(FilterDecorator):
    '''Class for filtering replays in urls'''

    def __init__(self, filter: FilterUrlsDTO) -> None:
        self.filter = filter

    def get_description(self) -> str:
        return self.filter.get_description() + ",Replays filter"

    def filtering(self, data: UrlsDTO = None) -> UrlsDTO:
        subset = set()
        result = UrlsDTO([])
        for elem in data:
            if elem in subset:
                continue
            subset.add(elem)
            result.add(elem)
        return result
