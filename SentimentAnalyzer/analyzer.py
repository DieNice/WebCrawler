from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from Mongodb.config import DevelopingConfig
from Mongodb.models import Page
import string
import nltk
import click
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import fasttext


class SentimentAnalyzer():
    def __init__(self):
        self.tokenizer = RegexTokenizer()
        fasttext.FastText.eprint = lambda x: None
        self.stop_words = stopwords.words('russian')

    def connect_to_db(self, namedb, usr, pwd, port):
        self.connect = DevelopingConfig(namedb, usr, pwd, port)

    def __get_data(self):
        return Page.objects()

    def __prepare(self, text):
        sentences = sent_tokenize(text)
        for i in range(len(sentences)):
            sentences[i] = sentences[i].replace('\n\n', '')
            tokens = word_tokenize(sentences[i])
            words = [word for word in tokens if word.isalpha()]
            words = [w for w in words if not w in self.stop_words]
            sentences[i] = " ".join(words)
        return sentences

    def analyze(self):
        pages = self.__get_data()
        with click.progressbar(pages, label="Sentiment analyse") as bar:
            for page in bar:
                model = FastTextSocialNetworkModel(tokenizer=self.tokenizer, lemmatize=True)
                sentences = self.__prepare(page.content)
                results = model.predict(sentences, k=2)
                count_positive = 0
                sum_positive = 0
                count_negative = 0
                sum_negative = 0
                count_neutral = 0
                sum_neutral = 0
                count_skip = 0
                sum_skip = 0
                for result in results:
                    if 'neutral' in result:
                        count_neutral += 1
                        sum_neutral += result['neutral']
                    if 'positive' in result:
                        count_positive += 1
                        sum_positive += result['positive']
                    if 'negative' in result:
                        count_negative += 1
                        sum_negative += result['negative']
                    if 'skip' in result:
                        count_skip += 1
                        sum_skip += result['skip']
                try:
                    result_positive = sum_positive / count_positive
                except ZeroDivisionError:
                    result_positive = 0
                try:
                    result_negative = sum_negative / count_negative
                except ZeroDivisionError:
                    result_negative = 0
                try:
                    result_neutral = sum_neutral / count_neutral
                except ZeroDivisionError:
                    result_neutral = 0
                try:
                    result_skip = sum_skip / count_skip
                except ZeroDivisionError:
                    result_skip = 0

                print(f"\n{page.title}")
                print(f"\nPositive:{result_positive}")
                print(f"\nNegative:{result_negative}")
                print(f"\nNeutral:{result_neutral}")
                print(f"\nSkip:{result_skip}")
                page.positive_sentiment = result_positive
                page.negative_sentiment = result_negative
                page.neutral_sentiment = result_neutral
                page.skip_sentiment = result_skip
                page.save()
