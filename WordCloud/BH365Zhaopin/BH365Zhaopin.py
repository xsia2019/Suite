# 查询北海365招聘网上的职位信息
# https://www.365zhaopin.com/
# author: kinofgl
# -*- coding: utf-8 -*-

import random
import re
import time
import csv
import requests
from bs4 import BeautifulSoup
from fake_user_agent.main import user_agent
from requests import RequestException
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, CardItem


class BH365Zhaopin(object):
    def __init__(self):
        self.url = 'https://www.365zhaopin.com/'
        self.headers = {'User-Agent': user_agent()}

    def get_html(self, url):
        while True:
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                return response.text
            except RequestException:
                print('网络错误，请重试')
                time.sleep(random.random() * 3)

    def get_page_num(self, html):
        while True:
            try:
                soup = BeautifulSoup(html, 'lxml')
                page_num = soup.select('span.ml20')[0].get_text()
                return int(page_num[2:5])
            except:
                return None

    def get_job_info(self, html):
        soup = BeautifulSoup(html, 'lxml')
        job_items = soup.select('div.w1024.f-yehei > div.main-ul > ul > li')
        job_info = []
        for job_item in job_items:
            job_name = job_item.find('div', class_='panl1').find('a').get_text().strip()
            job_company = job_item.find('div', class_='panl10 mt3').get_text().strip()
            job_time = job_item.find('div', class_='panl5').get_text().strip()
            job_url = self.url + job_item.find('div', class_='panl1').find('a')['href']
            job_salary = job_item.find('div', class_='panl3 salary-panl3').get_text().strip()
            if re.search(r'底薪\d{4,5}', job_salary):
                job_salary = re.search(r'(?<=底薪)\d{4,5}', job_salary).group()
            elif re.search(r'￥\d{4,5}', job_salary):
                job_salary = re.search(r'(?<=￥)\d{4,5}', job_salary).group()
            else:
                continue
            job_info.append([job_name, job_salary, job_company, job_time, job_url])
        return job_info

    def job_info_filter(self, list):
        salary_list = []
        for item in list:
            if int(item[1]) > 10000:
                if re.search(r'(助理)|(副)|(行政)|(主管)', item[0]):
                    salary_list.append(item)
        return salary_list

    def save_csv(self, job_info):
        today = time.strftime('%Y-%m-%d', time.localtime())
        filepath = 'BH365Zhaopin_' + today + '.csv'
        with open(filepath, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(job_info.values())

# 起始链接
start_page = r'https://www.365zhaopin.com/index.php?do=search&p='
# 存放职位信息的文件路径
csv_file = r'C:\Users\Michael\OneDrive\桌面\我的工作区\365job.csv'
zhapin = BH365Zhaopin()

# 解析第1页取得总页数
html = zhapin.get_html(start_page + '1')
page_num = zhapin.get_page_num(html)
print('总页数：', page_num)

my_job_info = []

# 解析第1-2页获取职位信息
for i in range(1, page_num + 1):
    html = zhapin.get_html(start_page + str(i))
    job_info = zhapin.get_job_info(html)
    job_info_filter = zhapin.job_info_filter(job_info)
    if len(job_info_filter) > 0:
        for item in job_info_filter:
            my_job_info.append(item)
    print('第', i, '/ %s 页解析完成' % page_num)
    time.sleep(random.random() * 3)

print(my_job_info)


# WebHook地址
webhook = r'https://oapi.dingtalk.com/robot/send?access_token' \
          r'=80da5c52f55d190c732e25b0d222249c2e509a29df36c78d3b389b14d211c724 '
# 机器人密钥
secret = r'SECf1d13f27bbceb66a187c37e1a4e422e87e52d7718727f3a548f9b9533b94c3c0'
# 可选：创建机器人勾选“加签”选项时使用

# 初始化机器人小丁
xiaoding = DingtalkChatbot(webhook, secret=secret)

xiaoding.send_markdown(title='今日天气', text=str(my_job_info), is_at_all=False)