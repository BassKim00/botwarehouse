from django import setup
import os
import numpy as np
import sys

if __name__ == "__main__":
    proj_path = "/Users/woong/Documents/mirae"
    sys.path.append(proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mirae.settings")
    setup()

import pandas as pd
import talib
from stock.models import *

class Indicator_macd():
    def __init__(self):
        self.data = {}

    def get_result_indicator(self, result, price, date, stock):
        rsi = Indicator_Macd(stock=stock, date=date, type=result, price=price)
        rsi.save()
        print({'result': result, 'price': price, 'date': date})

    def collect_regular_price_in_pandas(self, stock):
        # 이 함수는 일봉 데이터를 읽어온다
        price_data = Stock_Data.objects.filter(stock=stock).order_by('-id').all()
        # print(price_data)
        pandas_raw_data = {
            'high': [],
            'low': [],
            'close': [],
            'open': [],
            'date': [],
            'date_d': [],
        }
        for row in price_data:
            pandas_raw_data['high'].append(row.highest * 1.0)
            pandas_raw_data['low'].append(row.lowest * 1.0)
            pandas_raw_data['close'].append(row.close * 1.0)
            pandas_raw_data['open'].append(row.start * 1.0)
            pandas_raw_data['date'].append(row.date)
            pandas_raw_data['date_d'].append(row.date)

        df = pd.DataFrame(pandas_raw_data)
        df.set_index('date', inplace=True)
        df.sort_index(level='date', ascending=True, inplace=True)

        return df

    def ta_macd_indicator(self, stock):
        data = self.collect_regular_price_in_pandas(stock=stock)
        price_main = data.close
        date_main = data.date_d
        macd, macdsignal, macdhist = talib.MACD(price_main.values, fastperiod=12, slowperiod=26, signalperiod=9)
        # print(macd)
        # print(macdsignal)
        # print(macdhist)
        try:
            for i in range(1, len(macdhist)):
                if macdhist[i-1] > 0 and macdhist[i-2] < 0:
                    self.get_result_indicator('bid', price_main[i], date_main[i], stock)
                elif macdhist[i-1] < 0 and macdhist[i-2] > 0:
                    self.get_result_indicator('ask', price_main[i], date_main[i], stock)
        except Exception as e:
            print(e)
            print("-------------------------")
            # print(stock.name)
            # print(len(macdhist))
            # print(len(price_main))
            # print(len(date_main))
            print("-------------------------")
            pass
        
    def latest_ta_macd_indicator(self, stock):
        data = self.collect_regular_price_in_pandas(stock=stock)
        price_main = data.close
        date_main = data.date_d
        macd, macdsignal, macdhist = talib.MACD(price_main.values, fastperiod=12, slowperiod=26, signalperiod=9)
        # print(macd)
        # print(macdsignal)
        # print(macdhist)
        try:
            if macdhist[-1] > 0 and macdhist[-2] < 0:
                self.get_result_indicator('bid', price_main[-1], date_main[-1], stock)
            elif macdhist[-1] < 0 and macdhist[-2] > 0:
                self.get_result_indicator('ask', price_main[-1], date_main[-1], stock)
        except Exception as e:
            print(e)
            print("-------------------------")
            # print(stock.name)
            # print(len(macdhist))
            # print(len(price_main))
            # print(len(date_main))
            print("-------------------------")
            pass

if __name__ == '__main__':
    test = Indicator_macd()
    stocks = Stock.objects.exclude(code='000000').all()
    for stock in stocks:
        test.ta_macd_indicator(stock=stock)

