"""
用户认证视图模块
处理用户注册、登录和登出功能
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods


def register_view(request):
    """
    用户注册视图函数
    处理新用户注册
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "注册成功！")
            return redirect('static_pages:home')
    else:
        form = UserCreationForm()
    return render(request, 'user_auth/register.html', {'form': form})


def login_view(request):
    """
    用户登录视图函数
    处理用户登录认证
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"欢迎回来，{username}！")
                return redirect('static_pages:home')
    else:
        form = AuthenticationForm()
    return render(request, 'user_auth/login.html', {'form': form})


# 允许GET和POST方法
@require_http_methods(["GET", "POST"])
def logout_view(request):
    """
    用户登出视图函数
    处理用户登出，支持GET和POST请求
    """
    # 确保用户已登录
    if request.user.is_authenticated:
        # 执行登出操作
        logout(request)
        messages.info(request, "您已成功登出。")
    else:
        messages.warning(request, "您尚未登录。")
    
    # 重定向到首页
    return redirect('static_pages:home') 