from mongoengine import *


class DevelopingConfig():
    connect('crawlerdb', host='localhost', port=27017)
