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
            sensitive = sensitive.replace('[', '').replace(']', '').split(',')
            first = sensitive[0].replace('(', '').replace('\'', '')
            second = sensitive[2].replace('(', '').replace('\'', '').replace(' ', '')

            if first == "WR":
                first_idc = Indicator_Wr.objects.filter(stock=stock).order_by('-id').all()[0]
            elif first == "CROSS":
                first_idc = Indicator_Cross.objects.filter(stock=stock).order_by('-id').all()[0]
            elif first == "RSI":
                first_idc = Indicator_Rsi.objects.filter(stock=stock).order_by('-id').all()[0]
            elif first == "MACD":
                first_idc = Indicator_Macd.objects.filter(stock=stock).order_by('-id').all()[0]
            
            if second == "WR":
                second_idc = Indicator_Wr.objects.filter(stock=stock).order_by('-id').all()[0]
            elif second == "CROSS":
                second_idc = Indicator_Cross.objects.filter(stock=stock).order_by('-id').all()[0]
            elif second == "RSI":
                second_idc = Indicator_Rsi.objects.filter(stock=stock).order_by('-id').all()[0]
            elif second == "MACD":
                second_idc = Indicator_Macd.objects.filter(stock=stock).order_by('-id').all()[0]

            json = {
                'stock': stock.name,
                first: first_idc.type,
                second: second_idc.type
            }
            result_json.append(json)
        except Exception as e:
            print(e)
            pass

    return JsonResponse(result_json, safe=False)


def get_stock_list(request):
    print(request)
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

    print(result_json)

    return JsonResponse(result_json, safe=False)
