"""
汽车信息模型定义
"""
from django.db import models
from django.utils.text import slugify
from django.conf import settings
import os
import shutil


class Car(models.Model):
    """
    汽车信息模型
    存储汽车的详细信息，包括品牌、型号、价格、配置和图片
    """
    image = models.CharField(max_length=255, default='images/vehicles/benchiC.jpg')
    
    def get_image_url(self):
        from django.templatetags.static import static
        return static(self.image)

    def __eq__(self, other):
        return self.image == other.image 
            
    def __hash__(self):
        return hash(self.image) 
        
    
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='URL标识符')
    brand = models.CharField(max_length=100, verbose_name='品牌')
    model = models.CharField(max_length=100, verbose_name='型号')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    image = models.CharField(max_length=255, default='images/vehicles/benchiC.jpg', verbose_name='图片')
    
    # 新增字段
    year = models.IntegerField(verbose_name='年份', default=2024)
    engine = models.CharField(max_length=100, verbose_name='发动机', default='未知')
    transmission = models.CharField(max_length=50, verbose_name='变速箱', default='自动')
    fuel_type = models.CharField(max_length=50, verbose_name='燃料类型', default='汽油')
    mileage = models.IntegerField(verbose_name='里程数', default=0)
    color = models.CharField(max_length=50, verbose_name='颜色', default='黑色')
    description = models.TextField(verbose_name='描述', default='暂无描述')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '汽车'
        verbose_name_plural = '汽车列表'
        ordering = ['-created_at']
    
    def __str__(self):
        """返回模型的字符串表示"""
        return f"{self.brand} {self.model} ({self.year})"
    
    def save(self, *args, **kwargs):
        """重写save方法，自动生成slug"""
        if not self.slug:
            self.slug = slugify(f"{self.brand}-{self.model}-{self.year}")
        super().save(*args, **kwargs)
    
    @property
    def image_url(self):
        """获取图片URL"""
        # 直接返回静态文件路径
        return f'/static/{self.image}'
    
    @classmethod
    def create_from_json(cls, data):
        """从JSON数据创建或更新车辆记录"""
        # 处理图片
        image_name = data.pop('image', None)
        if image_name:
            # 如果是完整路径，获取文件名
            if '/' in image_name:
                image_name = os.path.basename(image_name)
            
            # 直接设置静态文件路径
            data['image'] = f'images/vehicles/{image_name}'
        else:
            # 使用默认图片
            data['image'] = 'images/vehicles/benchiC.jpg'
        
        # 获取或创建记录
        car, created = cls.objects.get_or_create(
            slug=data.get('slug'),
            defaults=data
        )
        
        return car, created 