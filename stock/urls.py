from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_stock_estimate', views.get_stock_estimate, name='get_stock_estimate'),
    path('get_stock_estimate_all', views.get_stock_estimate_all, name='get_stock_estimate_all'),
    path('get_stock_list', views.get_stock_list, name='get_stock_list'),
    path('add_stock_list', views.get_stock_list, name='get_stock_list'),
    path('remove_stock_list', views.get_stock_list, name='get_stock_list')

]