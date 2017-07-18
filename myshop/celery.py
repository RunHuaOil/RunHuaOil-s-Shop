from celery import Celery
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')

app.config_from_object('django.conf:settings')  # celery也可以在 django 的 settings 设置相应配置
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)  # celery 自动检查所有 app下 的 task.py 获取任务
