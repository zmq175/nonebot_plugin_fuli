import requests
from bs4 import BeautifulSoup


class Utility():
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
        }

    def get_html(self, url):
        response = requests.get(url, headers=self.headers)
        html = response.content.decode('utf-8')
        return html

    def get_random_img(self):
        start_url = "https://www.wnacg.com/albums-index-cate-3.html"
        start_soup = BeautifulSoup(self.get_html(start_url), 'lxml')
