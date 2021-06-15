from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, FloatField


class Page(Document):
    '''Page model'''
    title = StringField(required=True)
    content = StringField(required=True)
    retrieved = DateTimeField(default=datetime.now())
    positive_sentiment = FloatField()
    negative_sentiment = FloatField()
    neutral_sentiment = FloatField()
    skip_sentiment = FloatField()

    def __str__(self) -> str:
        return str(self.title)
