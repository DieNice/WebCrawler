import logging
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
from typing import Tuple
from operator import itemgetter


class SentimentAnalyzer():
    def __init__(self):
        self.tokenizer = RegexTokenizer()
        logging.info("set tokenizer")
        fasttext.FastText.eprint = lambda x: None
        self.stop_words = stopwords.words('russian')
        logging.info("set sropwords")

    def connect_to_db(self, namedb, usr, pwd, port):
        self.connect = DevelopingConfig(namedb, usr, pwd, port)
        logging.info("Sentiment analyzer connected to database")

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

    def __print_interpretation(self, pages: Page) -> None:
        '''Printed all sentiment values 4 kinds'''
        print("Interpritation:\n")
        for page in pages:
            print(f"\n{page.title}")
            print(f"\nPositive:{page.positive_sentiment}")
            print(f"\nNegative:{page.negative_sentiment}")
            print(f"\nNeutral:{page.neutral_sentiment}")
            print(f"\nSkip:{page.skip_sentiment}")
            logging.info(f"\n{page.title}")
            logging.info(f"\nPositive:{page.positive_sentiment}")
            logging.info(f"\nNegative:{page.negative_sentiment}")
            logging.info(f"\nNeutral:{page.neutral_sentiment}")
            logging.info(f"\nSkip:{page.skip_sentiment}")

    def __print_justification(self) -> None:
        ''':return justification of result'''
        result_list = []
        result_list.append((Page.objects.average('positive_sentiment'), 'Positive sentiment'))
        result_list.append((Page.objects.average('negative_sentiment'), 'Negative sentiment'))
        result_list.append((Page.objects.average('neutral_sentiment'), 'Neutral sentiment'))
        result_list.append((Page.objects.average('skip_sentiment'), 'Skip sentiment'))
        result_list.sort(key=itemgetter(0))
        print(
            f"Justification:{result_list[0][1]}({result_list[0][0]})<{result_list[1][1]}({result_list[1][0]})<{result_list[2][1]}({result_list[2][0]})<{result_list[3][1]}({result_list[3][0]})")
        logging.info(
            f"Justification:{result_list[0][1]}({result_list[0][0]})<{result_list[1][1]}({result_list[1][0]})<{result_list[2][1]}({result_list[2][0]})<{result_list[3][1]}({result_list[3][0]})")

    def __count_result_value(self) -> Tuple[float, str]:
        ''':return max sentiment value and description'''
        result_list = []
        result_list.append((Page.objects.average('positive_sentiment'), 'Positive sentiment'))
        result_list.append((Page.objects.average('negative_sentiment'), 'Negative sentiment'))
        result_list.append((Page.objects.average('neutral_sentiment'), 'Neutral sentiment'))
        result_list.append((Page.objects.average('skip_sentiment'), 'Skip sentiment'))
        maximum = -1
        description = ''
        for elem, desc in result_list:
            if elem > maximum:
                maximum = elem
                description = desc
        return maximum, description

    def analyze(self):
        pages = self.__get_data()
        with click.progressbar(pages, label="Sentiment analyse") as bar:
            for page in bar:
                model = FastTextSocialNetworkModel(tokenizer=self.tokenizer, lemmatize=True)
                sentences = self.__prepare(page.content)
                logging.info(f"page {page.title} prepared")
                results = model.predict(sentences, k=2)
                logging.info(f"page {page.title} predicted")
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
                logging.info(f"result positive value are counted {result_positive}")
                try:
                    result_negative = sum_negative / count_negative
                except ZeroDivisionError:
                    result_negative = 0
                logging.info(f"result negative value are counted {result_negative}")
                try:
                    result_neutral = sum_neutral / count_neutral
                except ZeroDivisionError:
                    result_neutral = 0
                logging.info(f"result neutral value are counted {result_neutral}")
                try:
                    result_skip = sum_skip / count_skip
                except ZeroDivisionError:
                    result_skip = 0
                logging.info(f"result skip value are counted {result_skip}")

                page.positive_sentiment = result_positive
                page.negative_sentiment = result_negative
                page.neutral_sentiment = result_neutral
                page.skip_sentiment = result_skip
                page.save()
                logging.info(f"results of sentiment values of {page.title} are saved")
        result_value, description = self.__count_result_value()
        print(f"{description}:{result_value}")
        logging.info(f'Culculated result sentiment value {result_value}({description})')
        self.__print_justification()
        self.__print_interpretation(pages)
