from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_stock_estimate/<int:user_id>', views.get_stock_estimate, name='get_stock_estimate'),
    path('get_stock_list', views.get_stock_list, name='get_stock_list')

]