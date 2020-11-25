from SearchResultsParser.SearchFacade import SearchFacade
from SearchResultsParser.abstract_parser import AbstractResultParser
from SearchResultsParser.google_parser import GoogleParser
from SearchResultsParser.rambler_parser import RamblerParser
from SearchResultsParser.replays_filter import ReplaysFilter
from SearchResultsParser.yandex_parser import YandexParser

if __name__ == '__main__':
    searchers: AbstractResultParser = []
    searchers.append(GoogleParser())
    searchers.append(YandexParser())
    searchers.append(RamblerParser())
    filter = ReplaysFilter()
    sf = SearchFacade(searchers, filter)
    print(sf.search_operation('Ашманов и компания', 10))
