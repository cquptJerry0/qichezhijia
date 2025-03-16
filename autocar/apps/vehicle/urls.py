"""
汽车信息模块URL配置
"""
from django.urls import path
from . import views

app_name = 'vehicle'

urlpatterns = [
    # 汽车列表
    path('', views.CarListView.as_view(), name='car_list'),
    # 收藏列表 - 注意：这个必须放在上面，否则会被下面的slug匹配规则捕获
    path('favorites/', views.FavoriteListView.as_view(), name='favorite_cars'),
    # 收藏功能
    path('favorite/toggle/<int:car_id>/', views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
    # 汽车详情 - 注意：这个必须放在最后，因为它会匹配所有的slug
    path('<slug:slug>/', views.CarDetailView.as_view(), name='car_detail'),
] 