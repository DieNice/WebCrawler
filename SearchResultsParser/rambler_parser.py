from .abstract_parser import AbstractResultParser


class RamblerParser(AbstractResultParser):
    def getquery(self, query: str) -> str:
        return "https://nova.rambler.ru/search?query=" + query
