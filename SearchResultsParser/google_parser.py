from .abstract_parser import AbstractResultParser


class GoogleParser(AbstractResultParser):
    def getquery(self, query: str) -> str:
        return query
