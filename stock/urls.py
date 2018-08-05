from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_stock_estimate/<int:user_id>', views.get_stock_estimate, name='get_stock_estimate'),
<<<<<<< HEAD
    path('get_stock_list', views.get_stock_list, name='get_stock_list')
=======
    path('get_user_stock/<int:user_id>', views.get_user_stock, name='get_user_stock')
>>>>>>> 1cc61e14af32193370e172206900c856bbd17bd7
]