from .abstract_parser import AbstractResultParser


class YandexParser(AbstractResultParser):
    def get_query(self, query: str) -> str:
        return "https://yandex.ru/search/?text=" + query

    def get_description(self) -> str:
        return "Yandex search engine"
