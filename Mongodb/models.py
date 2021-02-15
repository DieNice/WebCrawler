from mongoengine.document import Document
from mongoengine.fields import *
from datetime import datetime


class Page(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    retrieved = DateTimeField(default=datetime.now())
