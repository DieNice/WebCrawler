import logging
from mongoengine.connection import get_db, connect


class DevelopingConfig():
    '''Config for connection with database mongo'''

    def __init__(self, name_db, username, passw, port):
        self.database = name_db
        self.username = username
        self.password = passw
        self.port = port

    def check_connection(self) -> bool:
        try:
            connect("testdb", host="mongodb://" + self.username
                                   + ":" + self.password + "@localhost:"
                                   + str(self.port) + '/?authSource=admin')
            db = get_db()
            db.command('dbstats')
            logging.fatal("Database connected successfully")
            return True
        except Exception:
            logging.fatal("Database not connected")
            return False

    def connect(self) -> None:
        self.connection = connect(self.database, host="mongodb://" + self.username
                                                      + ":" + self.password + "@localhost:"
                                                      + str(self.port) + '/?authSource=admin')
