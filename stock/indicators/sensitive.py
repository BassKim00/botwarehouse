from django import setup
import os
import sys
import operator

if __name__ == "__main__":
    proj_path = "/Users/woong/Documents/mirae"
    sys.path.append(proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mirae.settings")
    setup()

from stock.models import *

class Senstive():
    def __init__(self):
        self.data = {}

    def get_sensitvie(self, stock):
        res = []
        indicatiors = Indicator_Result.objects.filter(stock=stock).all()
        sensitive = {}
        for idc in indicatiors:
            sensitive[idc.indicator] = idc.profit
        sensitive = sorted(sensitive.items(), key=operator.itemgetter(1), reverse=True)
        for stv in sensitive:
            res.append(stv[0])
        res = Indicator_Sensitive(stock=stock, sensitive=res)
        res.save()



if __name__ == '__main__':
    test = Senstive()
    stocks = Stock.objects.exclude(code='000000').all()
    for stock in stocks:
        test.get_sensitvie(stock=stock)

