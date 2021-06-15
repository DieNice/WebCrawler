from .abstract_parser import AbstractResultParser


class RamblerParser(AbstractResultParser):
    def get_query(self, query: str) -> str:
        return "https://nova.rambler.ru/search?query=" + query

    def get_description(self) -> str:
        return "Rambler search engine"
