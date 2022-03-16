import requests
import lxml
import bs4
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from BeihaiJobAPI import BeiHaiJobAPI
import csv

utctime = datetime.utcnow()
bjtime = utctime + timedelta(hours=8)
name1 = bjtime.strftime('%Y-%m-%d')
name2 = bjtime.strftime('%Y-%m-%d-%H%M%S')
#
# job = BeiHaiJobAPI()
#
# job_list = job.get_job_all()
# filename = name1 + '-job_title.csv'
#
# info_list = []
# for item in job_list:
#     info_list.append(item[0])
#
# with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(info_list)

filename = '2022-03-15-job_title.csv'
# 将上面得到的数据生成词云
text_from_file_with_apath = open(filename, encoding='utf-8').read()

wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all=True)

wl_space_split = " ".join(wordlist_after_jieba)

# stopwords = {}.fromkeys([line.rstrip() for line in open('stopwords.txt', encoding='utf-8')])
stopwords = open('stopwords.txt', encoding='utf-8').read()
stopwords = set(stopwords.split('\n'))

# my_wordcloud = WordCloud(font_path="msyh.ttf", width=1600, height=900).generate(wl_space_split)
my_wordcloud = WordCloud(stopwords=stopwords, font_path="msyh.ttf", collocations=True, width=1080, height=1920,
                         background_color='white', scale=3, ).generate(wl_space_split)

plt.imshow(my_wordcloud)
plt.axis("off")
plt.savefig(str(name2) + '.jpg', bbox_inches='tight', pad_inches=0, dpi=360)
# 输出图片并去除白边
