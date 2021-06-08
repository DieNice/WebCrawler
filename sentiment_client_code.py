from SentimentAnalyzer.analyzer import SentimentAnalyzer

if __name__ == '__main__':
    analyzer = SentimentAnalyzer()
    analyzer.connect_to_db('crawlerdb', 'root', 'root', 27017)
    analyzer.analyze()
