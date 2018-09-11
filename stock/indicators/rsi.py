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

class Indicator_rsi():
    def __init__(self):
        self.data = {}

    def get_result_indicator(self, result, price, date, stock):
        rsi = Indicator_Rsi(stock=stock, date=date, type=result, price=price)
        rsi.save()
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

    def ta_rsi_indicator(self, stock):
        data = self.collect_regular_price_in_pandas(stock=stock)
        price_main = data.close
        date_main = data.date_d

        rsi = talib.RSI(np.array(price_main.values, dtype=float), timeperiod=14)

        # print("-------------------------")
        # print(len(rsi))
        # print(len(price_main))
        # print(len(date_main))
        # print("-------------------------")
        try:
            for i in range(1, len(rsi)):
                if rsi[i] > 0:
                    if (rsi[i] <= 30) and (rsi[i - 1] > 30):
                        # print(self.get_result_indicator('bid', price_main[i], date_main[i], stock))
                        self.get_result_indicator('bid', price_main[i], date_main[i], stock)
                    elif (rsi[i] >= 70) and (rsi[i - 1] < 70):
                        # print(self.get_result_indicator('ask', price_main[i], date_main[i], stock))
                        self.get_result_indicator('ask', price_main[i], date_main[i], stock)
        except Exception as e:
            print(e)
            print("-------------------------")
            # print(stock.name)
            # print(len(rsi))
            # print(len(price_main))
            # print(len(date_main))
            print("-------------------------")
            pass
                # else:
                #     print(self.get_result_indicator('wait', price_main[i]))
    
    def latest_ta_rsi_indicator(self, stock):
        data = self.collect_regular_price_in_pandas(stock=stock)
        price_main = data.close
        date_main = data.date_d

        rsi = talib.RSI(np.array(price_main.values, dtype=float), timeperiod=14)

        # print("-------------------------")
        # print(len(rsi))
        # print(len(price_main))
        # print(len(date_main))
        # print("-------------------------")
        try:
            if rsi[-1] > 0:
                if (rsi[-1] <= 30) and (rsi[-2] > 30):
                    # print(self.get_result_indicator('bid', price_main[-1], date_main[-1], stock))
                    self.get_result_indicator('bid', price_main[-1], date_main[-1], stock)
                elif (rsi[-1] >= 70) and (rsi[-2] < 70):
                    # print(self.get_result_indicator('ask', price_main[-1], date_main[-1], stock))
                    self.get_result_indicator('ask', price_main[-1], date_main[-1], stock)
        except Exception as e:
            print(e)
            print("-------------------------")
            print(stock.name)
            print(len(rsi))
            print(len(price_main))
            print(len(date_main))
            print("-------------------------")
            pass

if __name__ == '__main__':
    test = Indicator_rsi()
    stocks = Stock.objects.exclude(code='000000').all()
    for stock in stocks:
        test.ta_rsi_indicator(stock=stock)

