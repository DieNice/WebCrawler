import requests
import os
import textwrap
from bs4 import BeautifulSoup as bs


class Grabber:
    url = ""
    filename = ""
    path = ""
    content_tags = ['p', r""]
    wrap = 80

    def __init__(self, url_address: str) -> None:
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

    def get_text(self) -> None:
        r = requests.get(self.url).text
        soup = bs(r, 'html.parser')
        result = soup.text
        self.write_in_file(result)

    def write_in_file(self, text):
        file = open(str(self.path) + '/' + str(self.filename), mode="a")
        file.write(text)
        file.close()
