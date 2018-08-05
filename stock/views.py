from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from stock.models import *


def index(request):
    return HttpResponse("Hello, world. You're at the data index.")


def get_stock_estimate(request):
    if request.method == 'GET':
        naver_id = request.GET['user_id']
    else:
        naver_id = 'uram999'
    user = User.objects.filter(naver_id=naver_id).all()[0]
    result_json = []
    stock_list = User_stock.objects.filter(user=user).all()
    for user_stock in stock_list:
        try:
            stock = user_stock.stock
            sensitive = Indicator_Sensitive.objects.filter(stock=stock).all()[0].sensitive

            sensitive = sensitive.replace('[', '').replace(']', '').replace(' ', '').replace('\'', '').split(',')
            bid = 0
            ask = 0

            score = [50, 30, 15, 5]
            for i in range(0, len(sensitive)):
                if sensitive[i] == "WR":
                    type = Indicator_Wr.objects.filter(stock=stock).order_by('-id').all()[0].type
                elif sensitive[i] == "CROSS":
                    type = Indicator_Cross.objects.filter(stock=stock).order_by('-id').all()[0].type
                elif sensitive[i] == "RSI":
                    type = Indicator_Rsi.objects.filter(stock=stock).order_by('-id').all()[0].type
                elif sensitive[i] == "MACD":
                    type = Indicator_Macd.objects.filter(stock=stock).order_by('-id').all()[0].type

                if type == 'ask':
                    ask+=score[i]
                else:
                    bid+=score[i]


            json = {
                'stock': stock.name,
                'ask': ask,
                'bid': bid
            }
            result_json.append(json)
        except Exception as e:
            print(e)
            pass

    return JsonResponse(result_json, safe=False)


def get_stock_list(request):
    result_json = []

    if request.method == 'GET':
        naver_id = request.GET['user_id']
    else:
        naver_id = 'uram999'

    user_info = User.objects.filter(naver_id=naver_id).first()
    stock_list = User_stock.objects.filter(user_id=user_info.id).all()

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

    return JsonResponse(result_json, safe=False)
