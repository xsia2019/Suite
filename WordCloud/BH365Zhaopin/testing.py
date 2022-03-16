\# -*- coding: utf-8 -*-

from WordCloud.BeihaiJob.BeihaiJobAPI import BeiHaiJobAPI
from datetime import datetime, timedelta
import csv

utctime = datetime.utcnow()
bjtime = utctime + timedelta(hours=8)
bjtime = bjtime.strftime('%Y-%m-%d-%H%M%S')

job = BeiHaiJobAPI()
urls = job.get_job_url()

filename = bjtime + '-job_url.csv'

with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(urls)


# text_from_file_with_apath = open('2022-03-14-160305-job.txt', encoding='utf-8').read()
#
# wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all=True)
#
# wl_space_split = " ".join(wordlist_after_jieba)
#
# # my_wordcloud = WordCloud(font_path="msyh.ttf", width=1600, height=900).generate(wl_space_split)
# my_wordcloud = WordCloud(font_path="msyh.ttf", collocations=False, width=1600, height=900,
#                          background_color='white', scale=5, ).generate(wl_space_split)
# # my_wordcloud = WordCloud(font_path="msyh.ttf", width=1600, height=900).generate_from_text(wl_space_split)
#
#
# plt.imshow(my_wordcloud)
# plt.axis("off")
# plt.savefig(bjtime + '.jpg', bbox_inches='tight', pad_inches=0, dpi=360)
# # 输出图片并去除白边

