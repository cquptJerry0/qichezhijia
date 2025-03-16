"""加载初始数据的管理命令"""
import os
import json
import shutil
import markdown
from django.core.management.base import BaseCommand
from django.conf import settings
from autocar.apps.vehicle.models import Car


class Command(BaseCommand):
    help = '加载初始数据，包括车辆数据和静态页面内容'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='清空现有数据后再加载',
        )
        parser.add_argument(
            '--skip-vehicles',
            action='store_true',
            help='跳过加载车辆数据',
        )
        parser.add_argument(
            '--skip-pages',
            action='store_true',
            help='跳过加载页面内容',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='显示详细日志',
        )
      

    def log(self, msg, style='success', verbose_only=False):
        """输出日志"""
        if verbose_only and not self.verbose:
            return
        
        if style == 'success':
            self.stdout.write(self.style.SUCCESS(msg))
        elif style == 'warning':
            self.stdout.write(self.style.WARNING(msg))
        elif style == 'error':
            self.stdout.write(self.style.ERROR(msg))
        else:
            self.stdout.write(msg)

    def load_vehicles_data(self, clear_existing=False):
        """加载车辆数据"""
        self.log("开始加载车辆数据...")
        
        # 构建数据文件路径
        data_file = os.path.join(settings.BASE_DIR, 'initial_resources', 'data', 'vehicles.json')
        self.log(f'数据文件路径: {data_file}', verbose_only=True)
        
        try:
            # 读取数据文件
            with open(data_file, 'r', encoding='utf-8') as f:
                vehicles_data = json.load(f)
            self.log(f'成功读取数据文件，包含 {len(vehicles_data)} 条记录', verbose_only=True)
            
            # 如果指定了clear参数，则清空现有数据
            if clear_existing:
                Car.objects.all().delete()
                self.log('已清空现有数据')
            
            # 确保静态目录存在
            static_vehicles_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'vehicles')
            os.makedirs(static_vehicles_dir, exist_ok=True)
            self.log(f'静态文件目录: {static_vehicles_dir}', verbose_only=True)
            
            # 复制所有图片文件到静态目录
            source_images_dir = os.path.join(settings.BASE_DIR, 'initial_resources', 'data', 'images')
            if os.path.exists(source_images_dir):
                for image in os.listdir(source_images_dir):
                    source = os.path.join(source_images_dir, image)
                    target = os.path.join(static_vehicles_dir, image)
                    if os.path.isfile(source):
                        shutil.copy2(source, target)
                        self.log(f'复制图片: {image}', verbose_only=True)
            
            # 创建或更新车辆数据
            created_count = 0
            updated_count = 0
            error_count = 0
            
            for data in vehicles_data:
                try:
                    self.log(
                        f'处理车辆: {data.get("brand")} {data.get("model")}',
                        verbose_only=True
                    )
                    
                    car, created = Car.objects.update_or_create(
                        slug=data.get('slug'),
                        defaults={
                            'brand': data.get('brand'),
                            'model': data.get('model'),
                            'price': data.get('price'),
                            'image': data.get('image'),
                            'year': data.get('year'),
                            'engine': data.get('engine'),
                            'transmission': data.get('transmission'),
                            'fuel_type': data.get('fuel_type'),
                            'mileage': data.get('mileage'),
                            'color': data.get('color'),
                            'description': data.get('description')
                        }
                    )
                    
                    if created:
                        created_count += 1
                        self.log(
                            f'创建新记录: {car.brand} {car.model}',
                            verbose_only=True
                        )
                    else:
                        updated_count += 1
                        self.log(
                            f'更新记录: {car.brand} {car.model}',
                            verbose_only=True
                        )
                
                except Exception as e:
                    error_count += 1
                    self.log(
                        f'处理记录时出错: {str(e)}',
                        style='error'
                    )
            
            # 输出统计信息
            self.log(
                f'车辆数据处理完成：新建 {created_count} 条，更新 {updated_count} 条'
                + (f'，失败 {error_count} 条' if error_count > 0 else '')
            )
            
        except FileNotFoundError:
            self.log(f'未找到车辆数据文件: {data_file}', style='error')
        except json.JSONDecodeError:
            self.log(f'车辆数据文件格式错误: {data_file}', style='error')
        except Exception as e:
            self.log(f'加载车辆数据时出错: {str(e)}', style='error')

    def load_pages_content(self):
        """加载静态页面内容"""
        self.log("开始加载静态页面内容...")
        
        # 构建页面目录路径
        pages_dir = os.path.join(settings.BASE_DIR, 'initial_resources', 'pages')
        self.log(f'页面目录路径: {pages_dir}', verbose_only=True)
        
        try:
            # 读取页面文件
            page_files = [f for f in os.listdir(pages_dir) if f.endswith('.md')]
            self.log(f'找到 {len(page_files)} 个页面文件', verbose_only=True)
            
            for page_file in page_files:
                try:
                    with open(os.path.join(pages_dir, page_file), 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 转换Markdown为HTML
                    html_content = markdown.markdown(content)
                    
                    # 获取页面名称
                    page_name = os.path.splitext(page_file)[0]
                    
                    self.log(f'处理页面: {page_name}', verbose_only=True)
                    
                    # 保存HTML内容到模板目录
                    templates_dir = os.path.join(settings.BASE_DIR, 'templates', 'static_pages')
                    os.makedirs(templates_dir, exist_ok=True)
                    
                    output_file = os.path.join(templates_dir, f"{page_name}.html")
                    
                    # 创建包含HTML内容的模板文件
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(f"""
{{% extends "base.html" %}}

{{% block title %}}{page_name.title()}{{% endblock %}}

{{% block content %}}
<div class="container mt-4">
    <div class="row">
        <div class="col-12">
            {html_content}
        </div>
    </div>
</div>
{{% endblock %}}
""")
                    
                    self.log(f'已生成页面模板: {output_file}')
                    
                except Exception as e:
                    self.log(f'处理页面文件 {page_file} 时出错: {str(e)}', style='error')
            
        except FileNotFoundError:
            self.log(f'未找到页面目录: {pages_dir}', style='error')
        except Exception as e:
            self.log(f'加载页面内容时出错: {str(e)}', style='error')

 
        """修复车辆图片路径"""
        self.log("开始修复车辆图片路径...")
        
        # 显示所有车辆的图片路径
        self.log("当前图片路径情况：")
        for car in Car.objects.all():
            self.log(f"{car.brand} {car.model}: {car.image}", verbose_only=True)

        # 设置每个车型对应的图片文件名 - 使用实际存在的文件名
        car_images = {
            'tesla-model-3': 'tesla3.jpg',
            'byd-han': 'bydhan.jpg',
            'li-auto-l9': 'lixiangL9.jpg',
            'mercedes-benz-c': 'benchiC.jpg',
            'bmw-3-series': 'baoma3.jpg',
            'audi-a4l': 'aodia4.jpg',
            'zeekr-001': 'jike001.jpg',
            'xpeng-p7': 'xiaopengP7.jpg',
            'hongqi-m7': 'wendingM7.jpg',
            'porsche-taycan': 'porscheTaycan.jpg'
        }

        # 图片处理
        # 更新车辆图片路径
        for car in Car.objects.all():
            # 构建用于匹配的键
            match_key = None
            
            # 尝试从slug中提取匹配键
            if car.slug:
                for key in car_images.keys():
                    if key in car.slug.lower():
                        match_key = key
                        break
            
            # 如果没有匹配到，尝试从品牌和型号匹配
            if not match_key:
                brand_model = f"{car.brand} {car.model}".lower()
                if '极氪' in car.brand or 'zeekr' in brand_model:
                    match_key = 'zeekr-001'
                elif '问界' in car.brand or 'm7' in brand_model:
                    match_key = 'hongqi-m7'
                elif '小鹏' in car.brand or 'xpeng' in brand_model or 'p7' in brand_model:
                    match_key = 'xpeng-p7'
                elif '保时捷' in car.brand or 'porsche' in brand_model or 'taycan' in brand_model:
                    match_key = 'porsche-taycan'
                elif '理想' in car.brand or 'li auto' in brand_model or 'l9' in brand_model:
                    match_key = 'li-auto-l9'
                elif '比亚迪' in car.brand or 'byd' in brand_model or '汉' in car.model:
                    match_key = 'byd-han'
                elif '特斯拉' in car.brand or 'tesla' in brand_model or 'model 3' in brand_model:
                    match_key = 'tesla-model-3'
                elif '奥迪' in car.brand or 'audi' in brand_model or 'a4' in brand_model:
                    match_key = 'audi-a4l'
                elif '宝马' in car.brand or 'bmw' in brand_model or '3系' in car.model:
                    match_key = 'bmw-3-series'
                elif '奔驰' in car.brand or 'mercedes' in brand_model or 'c' in car.model.lower():
                    match_key = 'mercedes-benz-c'
            
            # 如果仍然没有匹配到，使用默认图片
            if match_key:
                new_image = f"images/vehicles/{car_images[match_key]}"
            else:
                # 使用默认图片
                new_image = "images/vehicles/benchiC.jpg"
            
            # 更新图片路径
            old_image = car.image
            car.image = new_image
            car.save()
            
            self.log(f"已更新: {car.brand} {car.model}: {old_image} -> {new_image}")

        # 再次显示所有车辆的图片路径
        self.log("\n更新后的图片路径：")
        for car in Car.objects.all():
            self.log(f"{car.brand} {car.model}: {car.image}", verbose_only=True)
            self.log(f"图片URL: {car.image_url}", verbose_only=True)
        
        self.log("图片路径修复完成！")

        help = '从JSON文件加载初始用户数据'


    def handle(self, *args, **options):
        self.verbose = options['verbose']
        self.log('开始加载初始数据...')
        
        if not options['skip_vehicles']:
            self.load_vehicles_data(options['clear'])
        
        if not options['skip_pages']:
            self.load_pages_content()
        
        self.log('初始数据加载完成!')

        
 
        