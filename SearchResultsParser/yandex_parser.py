from .abstract_parser import AbstractResultParser


class YandexParser(AbstractResultParser):
    def getquery(self, query: str) -> str:
        return "https://yandex.ru/search/?text=" + query
