# coding=utf-8
from django.contrib import admin
from .models import Tag, Category, Post,Page
from django.contrib.auth.models import User

import sys;

reload(sys);
sys.setdefaultencoding("utf8")

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email')
    
admin.site.unregister(User)
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Page)
admin.site.register(Tag)
admin.site.register(Category)