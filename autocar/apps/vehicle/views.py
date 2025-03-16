"""
汽车信息视图模块
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Car


def car_list(request):
    """
    显示所有汽车信息列表
    """
    cars = Car.objects.all()
    return render(request, 'vehicle/car_list.html', {'cars': cars})


def car_detail(request, slug):
    """
    显示单个汽车的详细信息
    
    参数:
        slug: 汽车的URL标识符
    """
    car = get_object_or_404(Car, slug=slug)
    return render(request, 'vehicle/car_detail.html', {'car': car})


@login_required
def favorite_cars(request):
    """
    用户收藏的汽车列表，需要登录
    """
    # 简化版本，实际项目中需要关联用户与收藏车辆
    cars = Car.objects.all()[:3]
    return render(request, 'vehicle/favorite_cars.html', {'cars': cars}) 

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