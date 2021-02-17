from mongoengine import *


class DevelopingConfig():
    def __init__(self, namedb, username, passw, port):
        db = namedb
        username = username
        password = passw
        port = port
        connect(db, host="mongodb://" + username + ":" + password + "@localhost:" + str(port) + '/?authSource=admin')
