import os
from django import setup
import datetime
import time
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
excel insert
'''

class ExcelData:

    def __init__(self):
        pass

    def stock_news(self, stock):
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        urls = {
            "https://news.google.com/news/rss/search/section/q/" + stock.code + "?hl=ko&gl=KR&ned=kr",
        }

        unique_news = {}
        excludeKeywords = ["test"]

        for url in urls:
            d = feedparser.parse(url)

            for e in d.entries:
                remove = False
                for keyword in excludeKeywords:
                    if e.title.find(keyword) != -1:
                        remove = True
                        break
                if remove:
                    continue
                unique_news[e.link] = e.title

        for link, title in unique_news.items():
            body = "[" + title + "]" + '\n\n' + link
            Stock_News




if __name__ == '__main__':
    e = ExcelData()
    stocks = Stock.objects.exclude(code='000000').all()
    for stock in stocks:
        e.stock_news(stock)
        break
