from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from stock.models import *


def index(request):
    return HttpResponse("Hello, world. You're at the data index.")

def get_stock_estimate(user=None):
    reuslt_json = []
    stock_list = Stock.objects.all()
    for stock in stock_list:
        try:
            wr = Indicator_Wr.objects.filter(stock=stock).all()[0]
            macd = Indicator_Macd.objects.filter(stock=stock).all()[0]
            rsi = Indicator_Rsi.objects.filter(stock=stock).all()[0]

            json = {
                'stock': stock.name,
                'wr': wr.type,
                'macd': macd.type,
                'rsi': rsi.type
            }
            reuslt_json.append(json)
        except Exception as e:
            pass

    return HttpResponse(reuslt_json)