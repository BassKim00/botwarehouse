import os
from django import setup
import sys
import feedparser
import ssl

if __name__ == "__main__":
    proj_path = "/Users/woong/Documents/mirae"
    sys.path.append(proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mirae.settings")
    setup()

from stock.models import *

dir = os.path.dirname(__file__)
'''
NewsData insert
'''

class NewsData:

    def __init__(self):
        pass

    def stock_news(self, stock):
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        urls = {
            "https://news.google.com/news/rss/search/section/q/" + stock.code + "?hl=ko&gl=KR&ned=kr",
        }

        unique_news = {}
        includeKeywords = ["주식", "주가", "증권", "특징주", "분기", "실적", "시황", "투자", "추천주", "매출액", "이익", "코스피", "코스닥",
                           "관련주", "빅데이터", "매도", "매수", "종목", "공시", "체결", "대비", "체결", "신고가", "거래", "증시",
                           "자산", stock.name]

        for url in urls:
            d = feedparser.parse(url)

            for e in d.entries:
                remove = False
                for keyword in includeKeywords:
                    if e.title.find(keyword) != -1:
                        unique_news[e.link] = e.title
                        remove = True
                        break
                if remove:
                    continue
                # unique_news[e.link] = e.title

        for link, title in unique_news.items():
            try:
                # body = "[" + title + "]" + '\n\n' + link
                # print(body)
                news = Stock_News(stock=stock, link=link, title=title)
                news.save()
            except Exception as e:
                pass




if __name__ == '__main__':
    e = NewsData()
    stocks = Stock.objects.exclude(code='000000').all()
    for stock in stocks:
        e.stock_news(stock)
