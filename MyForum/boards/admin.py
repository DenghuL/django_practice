from django.contrib import admin
from .models import Board

# Register your models here.

admin.site.register(Board)  # 注册一个board模块，可以在后天管理中看到该模块
