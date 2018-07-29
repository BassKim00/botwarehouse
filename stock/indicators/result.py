from django import setup
import os
import sys

if __name__ == "__main__":
    proj_path = "/Users/woong/Documents/mirae"
    sys.path.append(proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mirae.settings")
    setup()

from stock.models import *

class Indicator_wr():
    def __init__(self):
        self.data = {}

    def get_result_indicator(self, stock):
        indicatiors = Indicator_Wr.objects.filter(stock=stock).all()
        stock_count = 0
        last_price = 0
        current_price = 1000000
        for wr in indicatiors:
            if wr.type == "bid":
                current_price -= wr.price
                stock_count += 1
            elif wr.type == "ask":
                if stock_count > 0:
                    current_price += wr.price
                    stock_count -= 1
            last_price = wr.price

        profit = (current_price+(stock_count*last_price) - 1000000)/1000000
        res = Indicator_Result(stock=stock, indicator='WR', profit=profit)
        res.save()


if __name__ == '__main__':
    test = Indicator_wr()
    stocks = Stock.objects.exclude(code='000000').all()
    for stock in stocks:
        test.get_result_indicator(stock=stock)

