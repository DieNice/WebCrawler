from .filter_decorator import FilterDecorator
from .filter_urlsdto import FilterUrlsDTO
from SearchResultsParser.urlsdto import UrlsDTO


class ReplaysFilter(FilterDecorator):
    def __init__(self, filter: FilterUrlsDTO):
        self.filter = filter

    def getDescription(self):
        return self.filter.getDescription() + ",Replays filter"

    def filtering(self, data: UrlsDTO = None) -> UrlsDTO:
        subset = set()
        result = UrlsDTO([])
        for elem in data:
            if elem in subset:
                continue
            subset.add(elem)
            result.add(elem)
        return result
