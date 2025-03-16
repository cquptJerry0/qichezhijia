"""
汽车信息管理界面配置
"""
from django.contrib import admin
from .models import Car
from django import forms
from django.utils.html import format_html


class CarAdminForm(forms.ModelForm):
    """自定义Car模型表单"""
    image_upload = forms.ImageField(label='上传图片', required=False, help_text='上传新图片将覆盖现有图片')
    
    class Meta:
        model = Car
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 将image字段添加预览功能
        if self.instance and self.instance.image:
            self.fields['image'].help_text = f'当前图片路径: {self.instance.image}'
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # 处理上传的图片
        if self.cleaned_data.get('image_upload'):
            uploaded_file = self.cleaned_data['image_upload']
            # 设置文件名为原始文件名
            filename = uploaded_file.name
            # 保存到images/vehicles/目录
            path = f'images/vehicles/{filename}'
            # 更新模型的image字段
            instance.image = path
            
            # 保存上传的文件到静态目录
            import os
            from django.conf import settings
            
            # 确保目录存在
            save_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'vehicles')
            os.makedirs(save_path, exist_ok=True)
            
            # 保存文件
            with open(os.path.join(save_path, filename), 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
        
        if commit:
            instance.save()
        return instance
      

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """汽车信息管理配置"""
    form = CarAdminForm
    list_display = ('brand', 'model', 'price', 'created_at', 'image_preview')
    list_filter = ('brand', 'created_at')
    search_fields = ('brand', 'model')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    def image_preview(self, obj):
        """显示图片预览"""
        if obj.image:
            return format_html('<img src="/static/{}" width="50" height="30" /><br>{}'.format(
                obj.image, '/static/' + obj.image))
        return '-'
    
    image_preview.short_description = '图片预览'
    
    readonly_fields = ('image_large_preview',)
    
    def image_large_preview(self, obj):
        """在编辑页面显示大图预览"""
        if obj.image:
            return format_html('<img src="/static/{}" width="300" style="max-height:200px" /><br>完整URL: /static/{}', 
                obj.image, obj.image)
        return '无图片'
    
    image_large_preview.short_description = '图片预览'
    
    fieldsets = (
        ('基本信息', {'fields': ('slug', 'brand', 'model', 'price', 'year')}),
        ('车辆图片', {'fields': ('image', 'image_upload', 'image_large_preview')}),
        ('详细配置', {'fields': ('engine', 'transmission', 'fuel_type', 'mileage', 'color')}),
        ('其他信息', {'fields': ('description',)}),
    )