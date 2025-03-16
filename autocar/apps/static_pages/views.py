"""
静态页面视图模块
负责渲染首页、关于和联系我们等静态页面
"""
import os
import markdown
from django.conf import settings
from django.shortcuts import render


def home(request):
    """
    首页视图函数
    显示网站首页内容和精选汽车
    """
    return render(request, 'static_pages/home.html')


def about(request):
    """
    关于页面视图函数
    从Markdown文件渲染关于页面内容
    """
    md_path = os.path.join(settings.BASE_DIR, 'initial_resources', 'pages', 'about.md')
    try:
        with open(md_path, 'r', encoding='utf-8') as file:
            content = file.read()
            html_content = markdown.markdown(content)
    except FileNotFoundError:
        html_content = "<p>关于页面内容暂时不可用。</p>"
    
    return render(request, 'static_pages/about.html', {'content': html_content})


def contact(request):
    """
    联系我们页面视图函数
    从Markdown文件渲染联系页面内容
    """
    md_path = os.path.join(settings.BASE_DIR, 'initial_resources', 'pages', 'contact.md')
    try:
        with open(md_path, 'r', encoding='utf-8') as file:
            content = file.read()
            html_content = markdown.markdown(content)
    except FileNotFoundError:
        html_content = "<p>联系页面内容暂时不可用。</p>"
    
    return render(request, 'static_pages/contact.html', {'content': html_content})


def error_404(request, exception=None):
    """
    404错误页面处理函数
    """
    return render(request, 'error.html', {'error_code': 404, 'error_message': '页面不存在'}, status=404)


def error_500(request, exception=None):
    """
    500错误页面处理函数
    """
    return render(request, 'error.html', {'error_code': 500, 'error_message': '服务器错误'}, status=500) 