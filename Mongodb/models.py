from mongoengine import *
from datetime import datetime


class Page(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    retrieved = DateTimeField(default=datetime.now())
    positive_sentiment = FloatField()
    negative_sentiment = FloatField()
    neutral_sentiment = FloatField()
    skip_sentiment = FloatField()

    def __str__(self):
        return self.title
