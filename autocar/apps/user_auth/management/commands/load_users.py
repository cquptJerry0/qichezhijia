"""
加载初始用户数据的管理命令
"""
import os
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    help = '从JSON文件加载初始用户数据'

    def handle(self, *args, **kwargs):
        # 清除现有用户数据
        User.objects.all().delete()
        
        # 创建管理员用户
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@qichezhijia.com',
            password='admin123456',  # 设置明文密码
            first_name='超级',
            last_name='管理员'
        )
        
        # 创建测试用户
        user = User.objects.create_user(
            username='test_user',
            email='test@qichezhijia.com',
            password='test123456',  # 设置明文密码
            first_name='测试',
            last_name='用户'
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'成功创建管理员用户(admin/admin123456)和测试用户(test_user/test123456)'
            )
        ) 