from .filter_decorator import FilterDecorator
from .filter_urlsdto import FilterUrlsDTO
from SearchResultsParser.urlsdto import UrlsDTO


class OfficalSiteFilter(FilterDecorator):
    def __init__(self, filter: FilterUrlsDTO, urlsite: str):
        self.filter = filter
        self.urloffsite = urlsite

    def getDescription(self):
        return self.filter.getDescription() + ",Offical site filter"

    def filtering(self, data: UrlsDTO = None) -> UrlsDTO:
        prevdata = self.filter.filtering(data)
        result: UrlsDTO = UrlsDTO([])
        for i in prevdata:
            if i.find(self.urloffsite) == -1:
                result.append(i)
        return result
