#_*_coding:utf-8_*_
from django.contrib import admin
from .models import Category,Server

# Register your models here.
admin.site.register(Category)
admin.site.register(Server)

