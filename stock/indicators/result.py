from django import setup
import os
import sys

if __name__ == "__main__":
    proj_path = "/Users/woong/Documents/mirae"
    sys.path.append(proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mirae.settings")
    setup()

from stock.models import *

class Indicator_Results():
    def __init__(self):
        self.data = {}

    def get_result_indicator(self, stock):
        indicatiors = Indicator_Cross.objects.filter(stock=stock).all()
        stock_count = 0
        last_price = 0
        current_price = 1000000
        for cross in indicatiors:
            if cross.type == "bid":
                current_price -= cross.price
                stock_count += 1
            elif cross.type == "ask":
                if stock_count > 0:
                    current_price += cross.price
                    stock_count -= 1
            last_price = cross.price
        profit = (current_price+(stock_count*last_price) - 1000000)/1000000
        res = Indicator_Result(stock=stock, indicator='CROSS', profit=profit, stock_count=stock_count,
                               last_price=last_price, current_price=current_price)
        res.save()

        indicatiors = Indicator_Rsi.objects.filter(stock=stock).all()
        stock_count = 0
        last_price = 0
        current_price = 1000000
        for rsi in indicatiors:
            if rsi.type == "bid":
                current_price -= rsi.price
                stock_count += 1
            elif rsi.type == "ask":
                if stock_count > 0:
                    current_price += rsi.price
                    stock_count -= 1
            last_price = rsi.price

        profit = (current_price + (stock_count * last_price) - 1000000) / 1000000
        res = Indicator_Result(stock=stock, indicator='RSI', profit=profit, stock_count=stock_count,
                               last_price=last_price, current_price=current_price)
        res.save()

        indicatiors = Indicator_Macd.objects.filter(stock=stock).all()
        stock_count = 0
        last_price = 0
        current_price = 1000000
        for macd in indicatiors:
            if macd.type == "bid":
                current_price -= macd.price
                stock_count += 1
            elif macd.type == "ask":
                if stock_count > 0:
                    current_price += macd.price
                    stock_count -= 1
            last_price = macd.price

        profit = (current_price + (stock_count * last_price) - 1000000) / 1000000
        res = Indicator_Result(stock=stock, indicator='MACD', profit=profit, stock_count=stock_count,
                               last_price=last_price, current_price=current_price)
        res.save()

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

        profit = (current_price + (stock_count * last_price) - 1000000) / 1000000
        res = Indicator_Result(stock=stock, indicator='WR', profit=profit, stock_count=stock_count,
                               last_price=last_price, current_price=current_price)
        res.save()

    def latest_result_indicator(self, stock):
        cross = Indicator_Cross.objects.filter(stock=stock).order_by('-id').all()[0]
        last_profit = Indicator_Result.objects.filter(stok=stock, indicator='CROSS').all()[0]
        stock_count = last_profit.stock_count
        last_price = last_profit.last_price
        current_price = last_profit.current_price
        if cross.price != last_price:
            if cross.type == "bid":
                current_price -= cross.price
                stock_count += 1
            elif cross.type == "ask":
                if stock_count > 0:
                    current_price += cross.price
                    stock_count -= 1
            last_price = cross.price

            profit = (current_price + (stock_count * last_price) - 1000000) / 1000000
            last_profit.stock_count = stock_count
            last_profit.last_price = last_price
            last_profit.current_price = current_price
            last_profit.profit = profit
            last_profit.save()

        rsi = Indicator_Rsi.objects.filter(stock=stock).order_by('-id').all()[0]
        last_profit = Indicator_Result.objects.filter(stok=stock, indicator='RSI').all()[0]
        stock_count = last_profit.stock_count
        last_price = last_profit.last_price
        current_price = last_profit.current_price
        if rsi.price != last_price:
            if rsi.type == "bid":
                current_price -= rsi.price
                stock_count += 1
            elif rsi.type == "ask":
                if stock_count > 0:
                    current_price += rsi.price
                    stock_count -= 1
            last_price = rsi.price

            profit = (current_price + (stock_count * last_price) - 1000000) / 1000000
            last_profit.stock_count = stock_count
            last_profit.last_price = last_price
            last_profit.current_price = current_price
            last_profit.profit = profit
            last_profit.save()

        macd = Indicator_Macd.objects.filter(stock=stock).order_by('-id').all()[0]
        last_profit = Indicator_Result.objects.filter(stok=stock, indicator='MACD').all()[0]
        stock_count = last_profit.stock_count
        last_price = last_profit.last_price
        current_price = last_profit.current_price
        if macd.price != last_price:
            if macd.type == "bid":
                current_price -= macd.price
                stock_count += 1
            elif macd.type == "ask":
                if stock_count > 0:
                    current_price += macd.price
                    stock_count -= 1
            last_price = macd.price

            profit = (current_price + (stock_count * last_price) - 1000000) / 1000000
            last_profit.stock_count = stock_count
            last_profit.last_price = last_price
            last_profit.current_price = current_price
            last_profit.profit = profit
            last_profit.save()

        wr = Indicator_Wr.objects.filter(stock=stock).order_by('-id').all()[0]
        last_profit = Indicator_Result.objects.filter(stok=stock, indicator='WR').all()[0]
        stock_count = last_profit.stock_count
        last_price = last_profit.last_price
        current_price = last_profit.current_price
        if wr.price != last_price:
            if wr.type == "bid":
                current_price -= wr.price
                stock_count += 1
            elif wr.type == "ask":
                if stock_count > 0:
                    current_price += wr.price
                    stock_count -= 1
            last_price = wr.price

            profit = (current_price + (stock_count * last_price) - 1000000) / 1000000
            last_profit.stock_count = stock_count
            last_profit.last_price = last_price
            last_profit.current_price = current_price
            last_profit.profit = profit
            last_profit.save()




if __name__ == '__main__':
    test = Indicator_Results()
    stocks = Stock.objects.exclude(code='000000').all()
    for stock in stocks:
        test.get_result_indicator(stock=stock)

