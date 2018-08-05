from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from stock.models import *


def index(request):
    return HttpResponse("Hello, world. You're at the data index.")

def get_stock_estimate(request, user_id=1):
    user = User.objects.filter(id=user_id).all()[0]
    reuslt_json = []
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
            reuslt_json.append(json)
        except Exception as e:
            print(e)
            pass

    return JsonResponse(reuslt_json, safe=False)

def get_user_stock(request, user_id=1):
    user = User.objects.filter(id=user_id).all()[0]
    reuslt_json = []
    stock_list = User_stock.objects.filter(user=user).all()
    for user_stock in stock_list:
        try:
            stock = user_stock.stock
            json = {
                'stock': stock.name
            }
            reuslt_json.append(json)
        except Exception as e:
            print(e)
            pass

        return JsonResponse(reuslt_json, safe=False)