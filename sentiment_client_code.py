import logging
from sentiment_analyzer.analyzer import SentimentAnalyzer
from mongodb.config import DevelopingConfig

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.NOTSET,
        filename="crawler_logs.log",
        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        datefmt='%H:%M:%S',
    )

    analyzer = SentimentAnalyzer()
    analyzer.connect_to_db('crawlerdb', 'root', 'root', 27017)
    analyzer.analyze()
