from __future__ import annotations

from abc import ABC, abstractmethod

from googlesearch import search

from .urlsdto import UrlsDTO


class AbstractResultParser(ABC):
    def search(self, query: str, tld: str, num: int, stop: int, pause: int) -> UrlsDTO:
        normilizequery: str = self.getquery(query)
        res = []
        for j in search(normilizequery, tld=tld, num=num, stop=stop, pause=pause):
            res.append(j)
        return UrlsDTO(res)

    @abstractmethod
    def getquery(self, query: str) -> str:
        pass
