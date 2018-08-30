import pandas as pd
from django import setup
import os, sys, re
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    proj_path = "/Users/leeuram/2018Project/botwarehouse"
    sys.path.append(proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mirae.settings")
    setup()

from stock.models import *


class InfoData:

    def __init__(self):
        pass

    def get_url(self, item_name, code):

        url = 'https://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
        print("요청 URL = {}".format(url))
        return url

    def getTypeData(self):
        rows = Stock.objects.exclude(code='000000').exclude(businessType='NULL')

        for row in rows:

            item_name = row.name
            print(row.name)

            url = self.get_url(item_name, row.code)

            df = pd.DataFrame()
            df = df.dropna()
            df = df.reset_index()
            df = df.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open', '고가': 'high', '저가': 'low',
                                    '거래량': 'volume'})

            print(df)
            # 데이터의 타입을 int형으로 바꿔줌
            df[['date','close', 'diff', 'open', 'high', 'low', 'volume']] \
                = df[['date','close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)
            # 컬럼명 'date'의 타입을 date로 바꿔줌
            #df['date'] = pd.to_datetime(df['date'])
            # # 일자(date)를 기준으로 오름차순 정렬
            #df = df.sort_values(by=['date'], ascending=True)


if __name__ == '__main__':
    e = InfoData()
    e.getTypeData()
