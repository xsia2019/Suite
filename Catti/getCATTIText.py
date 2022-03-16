# -*- coding=utf-8 -*-

import random
import re

import requests
import time
from fake_user_agent.main import user_agent
from bs4 import BeautifulSoup


class CattiAPI(object):
    def __init__(self):
        self.headers = {'User-Agent': user_agent()}  # 取得ua
        self.start_url = 'http://www.catticenter.com/tgmj/'
        self.homepage = 'http://www.catticenter.com/'
        self.ids = [3469, 3370, 3322, 3265, 3132, 2726, 2546,]

    def get_urls(self):
        urls= []
        for id in self.ids:
            url = self.start_url + str(id)
            urls.append(url)
        return urls

    #  根据url取得网页htm内容
    def get_html(self, url):
        # 尝试3次获取网页
        num = 0
        while True:
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
                return response.text
            except:
                num += 1
                print('第 %s 次获取网页内容失败，重新获取...' % num)
                # 尝试3次不成功则放弃
                if num < 3:
                    time.sleep(random.randint(1, 10))  # 随机休眠1-10秒
                    continue
                else:
                    break

    def get_soup(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        return soup

    # get title
    def get_title(self, url):
        soup = self.get_soup(url)
        title = soup.find('h1', class_='ui-article-title').text.strip()
        return title

    # get content
    def get_content(self, url):
        text = []

        soup = self.get_soup(url)
        # contents = soup.findAll('p', style="text-indent: 2em; line-height: 1.75em;")
        contents = soup.find('div', class_='ui-article-cont')

        for content in contents:

            text.append(content.get_text())

        return text


if __name__ == '__main__':
    catti = CattiAPI()
    urls = catti.get_urls()
    for url in urls:
        print(url)

        title = catti.get_title(url)
        title = title.replace('《', '').replace('》', '')

        content = catti.get_content(url)

        with open('Catti-%s.txt' % title, 'w', encoding='utf-8') as f:
            f.write(title+'\n')
            f.write('\n'.join(content))
            f.close()

