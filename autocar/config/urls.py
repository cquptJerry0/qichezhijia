"""
项目URL配置 - 模块化路由管理
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # 汽车信息相关路由
    path('vehicles/', include('autocar.apps.vehicle.urls', namespace='vehicle')), 
    # 用户认证相关路由
    path('user/', include('autocar.apps.user_auth.urls')),
    # 静态页面路由 (包括首页)
    path('', include('autocar.apps.static_pages.urls')),
]

# 自定义错误处理程序
handler404 = 'autocar.apps.static_pages.views.error_404'
handler500 = 'autocar.apps.static_pages.views.error_500'

# 开发环境下的媒体文件和静态文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 