from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('get_user_id', views.get_user_id, name='get_user_id'),

    path('get_stock_estimate', views.get_stock_estimate, name='get_stock_estimate'),
    path('get_stock_estimate_all', views.get_stock_estimate_all, name='get_stock_estimate_all'),

    path('get_stock_list', views.get_stock_list, name='get_stock_list'),
    path('add_stock_list', views.add_stock_list, name='add_stock_list'),
    path('search_stock_list', views.search_stock_list, name='search_stock_list'),
    path('update_stock_list', views.update_stock_list, name='update_stock_list'),

    path('get_stock_news', views.get_stock_news, name='get_stock_news')
]