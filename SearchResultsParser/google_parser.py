from .abstract_parser import AbstractResultParser


class GoogleParser(AbstractResultParser):
    def get_query(self, query: str) -> str:
        return query

    def get_description(self) -> str:
        return "Google search engine"
