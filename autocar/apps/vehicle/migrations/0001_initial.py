# Generated by Django 3.1.7 on 2025-03-16 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='URL标识符')),
                ('brand', models.CharField(max_length=100, verbose_name='品牌')),
                ('model', models.CharField(max_length=100, verbose_name='型号')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价格')),
                ('image', models.CharField(default='images/vehicles/benchiC.jpg', max_length=255, verbose_name='图片')),
                ('year', models.IntegerField(default=2024, verbose_name='年份')),
                ('engine', models.CharField(default='未知', max_length=100, verbose_name='发动机')),
                ('transmission', models.CharField(default='自动', max_length=50, verbose_name='变速箱')),
                ('fuel_type', models.CharField(default='汽油', max_length=50, verbose_name='燃料类型')),
                ('mileage', models.IntegerField(default=0, verbose_name='里程数')),
                ('color', models.CharField(default='黑色', max_length=50, verbose_name='颜色')),
                ('description', models.TextField(default='暂无描述', verbose_name='描述')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '汽车',
                'verbose_name_plural': '汽车列表',
                'ordering': ['-created_at'],
            },
        ),
    ]
