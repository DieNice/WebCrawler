from __future__ import annotations
import logging
from abc import ABC, abstractmethod
import click
from googlesearch import search
from .urlsdto import UrlsDTO


class AbstractResultParser(ABC):
    '''absctract result parser class'''
    def search(self, query: str, tld: str, num_res: int, stop: int, pause: int) -> UrlsDTO:
        ''':return UrlsDTO from query'''
        normilize_query: str = self.get_query(query)
        logging.info(f"new normalized query \"{normilize_query}\"")
        res = []
        urls = search(normilize_query, tld=tld, num=num_res, stop=stop, pause=pause)
        with click.progressbar(urls,
                               label=f"Getting start links {self.get_description()}") as all_urls:
            for url in all_urls:
                logging.info(f"got \"{url}\"")
                res.append(url)
        return UrlsDTO(res)

    @abstractmethod
    def get_query(self, query: str) -> str:
        '''abstract method return query'''

    @abstractmethod
    def get_description(self) -> str:
        '''abstract method return description of google engine'''
