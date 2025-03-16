"""
汽车信息应用URL配置
"""
from django.urls import path
from . import views

app_name = 'vehicle'

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('favorites/', views.favorite_cars, name='favorite_cars'),
    path('<slug:slug>/', views.car_detail, name='car_detail'),
] 