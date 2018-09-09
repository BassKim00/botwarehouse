from django import setup
import os
import sys

if __name__ == "__main__":
    proj_path = "/Users/woong/Documents/mirae"
    sys.path.append(proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mirae.settings")
    setup()

from stock.models import *


class Sensitive_Results():
    def __init__(self):
        self.data = {}

    def get_result_sensitive(self, stock):

        try:
            sensitive = Indicator_Sensitive.objects.filter(stock=stock).all()[0].sensitive

            sensitive = sensitive.replace('[', '').replace(']', '').replace(' ', '').replace('\'', '').split(',')
            bid = 0
            ask = 0

            for i in range(0, len(sensitive)):
                if sensitive[i] == "WR":
                    toplist = Indicator_Wr.objects.filter(stock=stock).order_by('-id').all()
                elif sensitive[i] == "CROSS":
                    toplist = Indicator_Cross.objects.filter(stock=stock).order_by('-id').all()
                elif sensitive[i] == "RSI":
                    toplist = Indicator_Rsi.objects.filter(stock=stock).order_by('-id').all()
                elif sensitive[i] == "MACD":
                    toplist = Indicator_Macd.objects.filter(stock=stock).order_by('-id').all()
                break

            score = [50, 30, 15, 5]
            stock_count = 0
            last_price = 0
            current_price = 1000000
            for top in toplist:
                for i in range(0, len(sensitive)):
                    try:
                        if sensitive[i] == "WR":
                            type = Indicator_Wr.objects.filter(stock=stock, date=top.date).order_by('-id').all()[0].type
                        elif sensitive[i] == "CROSS":
                            type = Indicator_Cross.objects.filter(stock=stock, date=top.date).order_by('-id').all()[0].type
                        elif sensitive[i] == "RSI":
                            type = Indicator_Rsi.objects.filter(stock=stock, date=top.date).order_by('-id').all()[0].type
                        elif sensitive[i] == "MACD":
                            type = Indicator_Macd.objects.filter(stock=stock, date=top.date).order_by('-id').all()[0].type

                        if type == 'ask':
                            ask += score[i]
                        elif type == 'bid':
                            bid += score[i]
                    except Exception as e:
                        pass

                if ask > bid and ask >= 60:
                    if stock_count > 0:
                        current_price += top.price
                        stock_count -= 1
                elif bid > ask and bid >= 60:
                    current_price -= top.price
                    stock_count += 1
                last_price = top.price

            profit = (current_price + (stock_count * last_price) - 1000000) / 1000000
            res = Indicator_Result(stock=stock, indicator='SENSITIVE', profit=profit, stock_count=stock_count,
                                   last_price=last_price, current_price=current_price)
            res.save()
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    test = Sensitive_Results()
    stocks = Stock.objects.exclude(code='000000').all()
    for stockz in stocks:
        if stockz.id>200:
            test.get_result_sensitive(stock=stockz)

