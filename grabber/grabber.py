import logging
import os
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Grabber:
    '''Class for scraping text from html pages'''
    filename = ""
    path = ""

    # def __init__(self) -> None:
    #     self.tor_requester = TorRequester(ctrl_pass='mypassword', n_requests=5)

    def get_text(self, url_address):
        ''':return parsed text from url by bs'''
        browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
        browser.get(url_address)
        response = browser.page_source.encode('utf-8')
        browser.quit()
        soup = bs(response, 'html.parser')
        result = soup.text
        return result

    def write_in_file(self, url_address, text):
        '''        Get path and filename for saving article by splitting URL.
               If the URL ends with some.html, then the previous (-2) element
               of the path is taken to form the path and
                the filename = some.html.txt respectively.'''
        url = url_address
        path_arr = url.split('/')
        if path_arr[-1] != '':
            self.filename = path_arr[-1] + ".txt"
            self.path = os.getcwd() + "/".join(path_arr[1:-1])
        else:
            self.filename = path_arr[-2] + ".txt"
            self.path = os.getcwd() + "/".join(path_arr[1:-2])
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(str(self.path) + '/' + str(self.filename), mode="a") as file:
            file.write(text)
            file.close()
