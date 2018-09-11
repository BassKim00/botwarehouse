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
from stock.indicators.result import *
from stock.indicators.golden_dead_cross import *
from stock.indicators.macd import *
from stock.indicators.rsi import *
from stock.indicators.williams_r import *
from stock.indicators.sensitive import *

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
            for page in range(1, 2):
                pg_url = '{url}&page={page}'.format(url=url, page=page)
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
            # print(df.tail(1).index.values[0])
            for idx in range(df.tail(1).index.values[0]):
                if idx == 0:
                    continue
                try:
                    stock_data = Stock_Data(stock=row, date=df.ix[idx, 'date'], start=df.ix[idx, 'open'], highest=df.ix[idx, 'high'],
                                                lowest=df.ix[idx, 'low'], close=df.ix[idx, 'close'], volume=df.ix[idx, 'volume'])
                    stock_data.save()
                except Exception as e:
                    pass

            # stock_data = Stock_Data(stock=row, date=df.ix[1, 'date'], start=df.ix[1, 'open'], highest=df.ix[1, 'high'],
            #                             lowest=df.ix[1, 'low'], close=df.ix[1, 'close'], volume=df.ix[1, 'volume'])
            # stock_data.save()
            #
            # cross = Indicator_cross()
            # cross.latest_ta_golden_indicator(row)
            # macd = Indicator_macd()
            # macd.latest_ta_macd_indicator(row)
            # rsi = Indicator_rsi()
            # rsi.latest_ta_rsi_indicator(row)
            # wr = Indicator_wr()
            # wr.latest_ta_wr_indicator(row)
            #
            # result = Indicator_Results()
            # result.latest_result_indicator(row)
            #
            # sensitive = Senstive()
            # sensitive.get_sensitvie(row)




if __name__ == '__main__':
    e = InfoData()
    e.getTypeData()
