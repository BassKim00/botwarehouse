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

class Indicator_wr():
    def __init__(self):
        self.data = {}

    def get_result_indicator(self, result, price, date, stock):
        wr = Indicator_Wr(stock=stock, date=date, type=result, price=price)
        wr.save()
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

    def ta_wr_indicator(self, stock):
        data = self.collect_regular_price_in_pandas(stock=stock)
        price_main = data
        date_main = data.date_d
        will_r = talib.WILLR(price_main['high'].values, price_main['low'].values, price_main['close'].values,
                             timeperiod=14)
        # print("-------------------------")
        # print(len(will_r))
        # print(len(price_main))
        # print(len(date_main))
        # print("-------------------------")

        try:
            for i in range(1, len(will_r)):
                if will_r[i-1] < -80 and will_r[i] > -80:
                    self.get_result_indicator('bid', price_main['close'][i], date_main[i], stock)
                elif will_r[i-1] > -20 and will_r[i] < -20:
                    self.get_result_indicator('ask', price_main['close'][i], date_main[i], stock)
        except Exception as e:
            print(e)
            print("-------------------------")
            # print(stock.name)
            # print(len(will_r))
            # print(len(price_main))
            # print(len(date_main))
            print("-------------------------")
            pass

    def latest_ta_wr_indicator(self, stock):
        data = self.collect_regular_price_in_pandas(stock=stock)
        price_main = data
        date_main = data.date_d
        will_r = talib.WILLR(price_main['high'].values, price_main['low'].values, price_main['close'].values,
                             timeperiod=14)
        print("-------------------------")
        print(len(will_r))
        print(len(price_main))
        print(len(date_main))
        print("-------------------------")

        try:
            if will_r[-2] < -80 and will_r[-1] > -80:
                self.get_result_indicator('bid', price_main['close'][-1], date_main[-1], stock)
            elif will_r[-2] > -20 and will_r[-1] < -20:
                self.get_result_indicator('ask', price_main['close'][-1], date_main[-1], stock)
        except Exception as e:
            print(e)
            print("-------------------------")
            print(stock.name)
            print(len(will_r))
            print(len(price_main))
            print(len(date_main))
            print("-------------------------")
            pass

if __name__ == '__main__':
    test = Indicator_wr()
    stocks = Stock.objects.exclude(code='000000').all()
    for stock in stocks:
        test.ta_wr_indicator(stock=stock)

