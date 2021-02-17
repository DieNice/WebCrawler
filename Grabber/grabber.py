import os
from bs4 import BeautifulSoup as bs
from TorRequester.torrequester import TorRequester


class Grabber:
    url = ""
    filename = ""
    path = ""

    def __init__(self) -> None:
        self.torrequester = TorRequester(ctrl_pass='mypassword', n_requests=5)

    def get_text(self, url_address):
        self.url = url_address
        response = self.torrequester.get(self.url)
        soup = bs(response, 'html.parser')
        result = soup.text
        return result

    def write_in_file(self, url_address, text):
        '''        Get path and filename for saving article by splitting URL.
               If the URL ends with some.html, then the previous (-2) element
               of the path is taken to form the path and the filename = some.html.txt respectively.'''
        self.url = url_address
        path_arr = self.url.split('/')
        if path_arr[-1] != '':
            self.filename = path_arr[-1] + ".txt"
            self.path = os.getcwd() + "/".join(path_arr[1:-1])
        else:
            self.filename = path_arr[-2] + ".txt"
            self.path = os.getcwd() + "/".join(path_arr[1:-2])
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        file = open(str(self.path) + '/' + str(self.filename), mode="a")
        file.write(text)
        file.close()
