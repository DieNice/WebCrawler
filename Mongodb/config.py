from mongoengine import connect


class DevelopingConfig():
    '''Config for connection with database mongo'''

    def __init__(self, name_db, username, passw, port):
        self.database = name_db
        self.username = username
        self.password = passw
        self.port = port
        connect(self.database, host="mongodb://" + self.username
                                    + ":" + self.password + "@localhost:"
                                    + str(self.port) + '/?authSource=admin')
