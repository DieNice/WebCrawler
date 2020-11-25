from .interface_filter_urlsdto import InterfaceFilterUrlsDTO
from .urlsdto import UrlsDTO


class ReplaysFilter(InterfaceFilterUrlsDTO):
    def filtering(self, data: UrlsDTO) -> UrlsDTO:
        subset = set()
        result = UrlsDTO([])
        for elem in data:
            if elem in subset:
                continue
            subset.add(elem)
            result.add(elem)
        return result
