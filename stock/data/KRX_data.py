import pandas as pd
from django import setup
import os, sys, re
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    proj_path = "/Users/woong/Documents/mirae"
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
            # print(url)
            df = pd.DataFrame()

            pg_url = '{url}&page={page}'.format(url=url, page=1)
            df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

            df = df.dropna()
            df = df.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open', '고가': 'high', '저가': 'low',
                                    '거래량': 'volume'})
            # 데이터의 타입을 int형으로 바꿔줌
            df[['close', 'diff', 'open', 'high', 'low', 'volume']] \
                = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)
            # print(df)
            # 컬럼명 'date'의 타입을 date로 바꿔줌
            df['date'] = pd.to_datetime(df['date'])
            # # # 일자(date)를 기준으로 오름차순 정렬
            df = df.sort_values(by=['date'], ascending=False)
            stock_data = Stock_Data(stock=row, date=df.ix[1, 'date'], start=df.ix[1, 'open'], highest=df.ix[1, 'high'],
                                        lowest=df.ix[1, 'low'], close=df.ix[1, 'close'], volume=df.ix[1, 'volume'])
            stock_data.save()



if __name__ == '__main__':
    e = InfoData()
    e.getTypeData()
