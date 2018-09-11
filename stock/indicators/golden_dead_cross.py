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

class Indicator_cross():
    def __init__(self):
        self.data = {}

    def get_result_indicator(self, result, price, date, stock):
        cross = Indicator_Cross(stock=stock, date=date, type=result, price=price)
        cross.save()
        # print({'result': result, 'price': price, 'date': date})
        return {'result': result, 'price': price, 'date': date}

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
    def ta_golden_indicator(self, stock):
        data = self.collect_regular_price_in_pandas(stock=stock)
        price_main = data.close
        date_main = data.date_d

        ma5 = talib.SMA(price_main, timeperiod=5)
        ma20 = talib.SMA(price_main, timeperiod=10)
        ma60 = talib.SMA(price_main, timeperiod=60)
        try:
            for i in range(1, len(ma5)):
                if ma5[i-1] < ma60[i-1] and ma5[i] > ma60[i]:
                    if ma20[i] > ma60[i]:
                        self.get_result_indicator('bid', price_main[i], date_main[i], stock)
                elif ma5[i-1] > ma60[i-1]  and ma5[i] < ma60[i]:
                    if ma20[i] < ma60[i]:
                        self.get_result_indicator('ask', price_main[i], date_main[i], stock)
        except Exception as e:
            print(e)
            print("-------------------------")
            # print(stock.name)
            # print(len(price_main))
            # print(len(date_main))
            print("-------------------------")
            pass

    def latest_ta_golden_indicator(self, stock):
        data = self.collect_regular_price_in_pandas(stock=stock)
        price_main = data.close
        date_main = data.date_d

        ma5 = talib.SMA(price_main, timeperiod=5)
        ma20 = talib.SMA(price_main, timeperiod=10)
        ma60 = talib.SMA(price_main, timeperiod=60)
        try:
            if ma5[-2] < ma60[-2] and ma5[-1] > ma60[-1]:
                if ma20[-1] > ma60[-1]:
                    self.get_result_indicator('bid', price_main[-1], date_main[-1], stock)
            elif ma5[-2] > ma60[-2]  and ma5[-1] < ma60[-1]:
                if ma20[-1] < ma60[-1]:
                    self.get_result_indicator('ask', price_main[-1], date_main[-1], stock)
        except Exception as e:
            print(e)
            print("-------------------------")
            print(stock.name)
            print(len(price_main))
            print(len(date_main))
            print("-------------------------")
            pass


if __name__ == '__main__':
    test = Indicator_cross()
    stocks = Stock.objects.exclude(code='000000').all()
    for stock in stocks:
        test.ta_golden_indicator(stock=stock)
