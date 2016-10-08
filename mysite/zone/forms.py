# coding=utf-8
from django import forms
from .models import Post
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'category')
        labels = {
            'category': '分类目录',
            'text': '正文',
            'title': '标题',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 15}),
        }
		
class UserForm(forms.Form):
	username = forms.CharField(label='用户名：',max_length=100)
	passworld = forms.CharField(label='密码：',widget=forms.PasswordInput())
	email = forms.EmailField(label='电子邮件：')