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
            wr = Indicator_Wr.objects.filter(stock=stock).last()
            macd = Indicator_Macd.objects.filter(stock=stock).last()
            rsi = Indicator_Rsi.objects.filter(stock=stock).last()

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


def get_stock_list(request):
    print(request)
    result_json = []

    if request.method == 'GET':
        naver_id = request.GET['user_id']
    else:
        naver_id = 'uram999'

    user_id = User.objects.filter(naver_id=naver_id)
    print(user_id.id)
    stock_list = User_stock.objects.filter(user_id=user_id.id).all()

    for stock in stock_list:
        try:
            stock_data = Stock.objects.filter(id=stock.stock_id).first()

            json = {
                'stock_name': stock_data.name,
                'stock_code': stock_data.code,
                'stock_busiType': stock_data.businessType
            }
            result_json.append(json)

        except Exception as e:
            pass

    print(result_json)

    return HttpResponse(result_json)