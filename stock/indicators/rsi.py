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

    def get_result_indicator(self, result, price):
        return {'result': result, 'price': price}

    def collect_regular_price_in_pandas(self, stock):
        # 이 함수는 일봉 데이터를 읽어온다
        price_data = Stock_Data.objects.filter(stock=stock).order_by('-id').all()
        return price_data

    def ta_rsi_indicator(self, stock):
        price_main = self.collect_regular_price_in_pandas(stock=stock)
        print(np.array(price_main.values))
        rsi = talib.RSI(np.array(price_main.values, dtype=float), timeperiod=14)
        rsi = rsi[-2:]

        for i in range(1, len(rsi)):
            if (rsi[i] <= 30) and (rsi[i - 1] > 30):
                return self.get_result_indicator('bid', price_main[-1])
            elif (rsi[i] >= 70) and (rsi[i - 1] < 70):
                return self.get_result_indicator('ask', price_main[-1])
            # else:
                # return self.get_result_indicator('wait', price_main[-1])


if __name__ == '__main__':
    test = Indicator_rsi()
    test.ta_rsi_indicator(stock=1)

