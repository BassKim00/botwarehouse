from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from stock.models import *
from stock.data.news import NewsData


def index(request):
    return HttpResponse("Hello, world. You're at the data index.")


def get_user_id(request):
    if request.method == 'GET':
        fb_id = request.GET['fb_id']
    else:
        fb_id = '2163947200343823'

    user = User.objects.filter(fb_id=fb_id).first()

    json = {
        'naver_id': user.naver_id,
    }

    return JsonResponse(json, safe=False)


def get_stock_estimate(request):

    if request.method == 'GET':
        naver_id = request.GET['user_id']
        stock_code = request.GET['code']
    else:
        naver_id = 'uram999'

    stock = Stock.objects.filter(code=stock_code).first()
    user = User.objects.filter(naver_id=naver_id).first()

    user_stock = User_stock.objects.filter(stock_id=stock.id).filter(user_id=user.id).all()[0]
    result_json = []

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
                ask += score[i]
            else:
                bid += score[i]

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


def get_stock_estimate_all(request):

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

    user_info = User.objects.filter(naver_id=naver_id).first()
    stock_list = User_stock.objects.filter(user_id=user_info.id).all()

    for stock in stock_list:
        try:
            stock_data = Stock.objects.filter(id=stock.stock_id).first()

            json = {
                'stock_id': stock_data.id,
                'stock_name': stock_data.name,
                'stock_code': stock_data.code,
                'stock_busiType': stock_data.businessType
            }
            result_json.append(json)

        except Exception as e:
            pass

    return JsonResponse(result_json, safe=False)


def search_stock_list(request):
    result_json = []

    if request.method == 'GET':
        stock_code = request.GET['code']

    stock_info = Stock.objects.filter(code=stock_code).first()

    try:
        if isinstance(stock_info, type(None)):
            json = {
                'success': False,
                'msg': "Not Vaild Code"
            }
        else:
            json = {
                'success': True,
                'stock_code': stock_info.code,
                'stock_name': stock_info.name,
                'stock_type': stock_info.businessType
            }

        result_json.append(json)

    except Exception as e:
        print(e)
        pass

    return JsonResponse(result_json, safe=False)


def add_stock_list(request):
    result_json = []

    if request.method == 'GET':
        naver_id = request.GET['user_id']
        stock_code = request.GET['code']

    stock_info = Stock.objects.filter(code=stock_code).first()
    user_info = User.objects.filter(naver_id=naver_id).first()

    try:
        user_stock = User_stock.objects.filter(stock_id='639').filter(user_id=user_info.id).first()
        user_stock.stock_id = stock_info.id
        user_stock.save()

        json = {
            'success': True,
            'stock_code': stock_info.code,
            'stock_name': stock_info.name,
            'stock_type': stock_info.businessType
        }

        result_json.append(json)

    except Exception as e:
        print(e)
        pass

    return JsonResponse(result_json, safe=False)


def update_stock_list(request):
    result_json = []

    if request.method == 'GET':
        naver_id = request.GET['user_id']
        new_stock_code = request.GET['new_code']
        pre_stock_code = request.GET['pre_code']

    user_info = User.objects.filter(naver_id=naver_id).first()
    new_stock_info = Stock.objects.filter(code=new_stock_code).first()
    pre_stock_info = Stock.objects.filter(code=pre_stock_code).first()

    try:
        user_stock = User_stock.objects.filter(stock_id=pre_stock_info.id).filter(user_id=user_info.id).first()
        print(user_stock.stock_id)
        user_stock.stock_id = new_stock_info.id
        user_stock.save()

        json = {
            'success': True,
            'new_stock': {
                'stock_code': new_stock_info.code,
                'stock_name': new_stock_info.name,
                'stock_type': new_stock_info.businessType
            },
            'pre_stock' :{
                'stock_code': pre_stock_info.code,
                'stock_name': pre_stock_info.name,
                'stock_type': pre_stock_info.businessType
            }
        }

        result_json.append(json)

    except Exception as e:
        print(e)
        pass

    return JsonResponse(result_json, safe=False)


def get_stock_news(request):
    result_json = []

    if request.method == 'GET':
        code = request.GET['code']
    else:
        code = '021240'

    stock = Stock.objects.filter(code=code).all()[0]
    e = NewsData()
    e.stock_news(stock=stock)
    news = Stock_News.objects.filter(stock=stock).order_by('-id').all()
    i = 0
    for n in news:
        try:
            json = {
                'title': n.title,
                'link': n.link
            }
            result_json.append(json)

        except Exception as e:
            pass
        i = i+1
        if i == 5:
            break

    return JsonResponse(result_json, safe=False)