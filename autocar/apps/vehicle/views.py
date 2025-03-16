"""
汽车信息视图模块
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse
from .models import Car, Favorite
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse


class CarListView(View):
    """汽车列表视图"""
    def get(self, request):
        # 获取所有汽车
        cars = Car.objects.all()
        
        # 获取用户收藏的汽车ID列表
        favorite_car_ids = []
        if request.user.is_authenticated:
            favorite_car_ids = Favorite.objects.filter(user=request.user).values_list('car_id', flat=True)
        
        # 传递到模板
        context = {
            'cars': cars,
            'favorite_car_ids': favorite_car_ids,
        }
        return render(request, 'vehicle/car_list.html', context)


class CarDetailView(View):
    """汽车详情视图"""
    def get(self, request, slug):
        # 获取指定汽车
        car = get_object_or_404(Car, slug=slug)
        
        # 检查用户是否已收藏该车
        is_favorite = False
        if request.user.is_authenticated:
            is_favorite = Favorite.objects.filter(user=request.user, car=car).exists()
        
        # 传递到模板
        context = {
            'car': car,
            'is_favorite': is_favorite,
        }
        return render(request, 'vehicle/car_detail.html', context)


@method_decorator(login_required, name='dispatch')
class ToggleFavoriteView(View):
    """添加或移除收藏"""
    def post(self, request, car_id):
        car = get_object_or_404(Car, id=car_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, car=car)
        
        if not created:
            # 如果已经收藏，则取消收藏
            favorite.delete()
            is_favorite = False
            message = f"已取消收藏 {car.brand} {car.model}"
        else:
            is_favorite = True
            message = f"已收藏 {car.brand} {car.model}"
        
        # 如果是AJAX请求，返回JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'is_favorite': is_favorite,
                'message': message
            })
        
        # 普通请求，添加消息并重定向
        messages.success(request, message)
        
        # 返回到上一页或车辆详情页
        return redirect(request.META.get('HTTP_REFERER', reverse('vehicle:car_detail', args=[car.slug])))


@method_decorator(login_required, name='dispatch')
class FavoriteListView(View):
    """收藏列表视图"""
    def get(self, request):
        # 获取用户收藏的所有汽车
        favorites = Favorite.objects.filter(user=request.user).select_related('car')
        cars = [favorite.car for favorite in favorites]
        
        context = {
            'cars': cars,
        }
        return render(request, 'vehicle/favorite_cars.html', context)

def some_context_processor(request):
    # 确保这里没有尝试访问car.image.url
    # ...
    return context 

def vehicle_detail(request, slug):
    car = get_object_or_404(Car, slug=slug)
    print(f"Car type: {type(car)}")
    print(f"Car __dict__: {car.__dict__}")
    
    # 检查car对象的image属性
    print(f"Car image type: {type(car.image)}")
    print(f"Car image dir: {dir(car.image)}")
    
    # 不要尝试访问car.image.url，因为image是CharField
    
    # 重要：检查这里是否有其他上下文变量
    similar_cars = Car.objects.filter(brand=car.brand).exclude(id=car.id)[:3]
    
    context = {
        'car': car,
        'similar_cars': similar_cars,
        # 检查是否有类似以下的变量
        # 'car_image_url': car.image.url,  # 错误
    }
    
    return render(request, 'vehicle_detail.html', context) 

def some_context_processor(request):
    # 确保这里没有尝试访问car.image.url
    # ...
    return context 