from search_results_parser.urlsdto import UrlsDTO
from .filter_decorator import FilterDecorator
from .filter_urlsdto import FilterUrlsDTO


class OfficalSiteFilter(FilterDecorator):
    '''Class for filtering official page of company'''

    def __init__(self, urls_filter: FilterUrlsDTO, urlsite: str) -> None:
        self.filter = urls_filter
        self.url_offsite = urlsite

    def get_description(self) -> str:
        return self.filter.get_description() + ",Offical site filter"

    def filtering(self, data: UrlsDTO = None) -> UrlsDTO:
        prevdata = self.filter.filtering(data)
        result: UrlsDTO = UrlsDTO([])
        for url in prevdata:
            if url.find(self.url_offsite) == -1:
                result.append(url)
        return result
