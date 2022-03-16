import requests
import lxml
import bs4
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba

utctime = datetime.utcnow()
bjtime = utctime + timedelta(hours=8)
bjtime = bjtime.strftime('%Y-%m-%d')

# 将上面得到的数据生成词云
text_from_file_with_apath = open('2021年政府工作报告.txt', encoding='utf-8').read()
stopwords = open('stopwords.txt', encoding='utf-8').read()
stopwords = set(stopwords.split('\n'))

wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all=True)

wl_space_split = " ".join(wordlist_after_jieba)

# stopwords = {}.fromkeys([line.rstrip() for line in open('stopwords.txt', encoding='utf-8')])

# my_wordcloud = WordCloud(font_path="msyh.ttf", width=1600, height=900).generate(wl_space_split)
my_wordcloud = WordCloud(stopwords=stopwords, font_path="msyh.ttf", collocations=False, width=1800, height=766,
                         background_color='white', scale=4, ).generate(wl_space_split)

plt.imshow(my_wordcloud)
plt.axis("off")
plt.savefig(str(bjtime) + '.jpg', bbox_inches='tight', pad_inches=0, dpi=360)
# 输出图片并去除白边
