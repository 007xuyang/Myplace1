# coding=utf-8
from django.conf.urls import patterns, include, url
from . import views
from .views import *

urlpatterns = patterns('',
	url(r'^$',views.first_page,name='blog_index'),
    url(r'^post/list/$', views.post_list,name='post_list'),
	url(r'^post/(?P<pk>[0-9]+)/$',views.post_detail),
	url(r'^post/new/$',views.post_new,name='post_new'),
	url(r'^post/(?P<pk>[0-9]+)/edit/$',views.post_edit,name='post_edit'),
	url(r'^draft/$',views.post_draft_list,name='post_draft_list'),
	url(r'^post/(?P<pk>[0-9]+)/publish/$', views.post_publish, name='post_publish'),
	url(r'^post/(?P<pk>[0-9]+)/remove/$',views.post_remove,name='post_remove'),
	url(r'^post/search/$', full_search, name='full_search'),
	url(r'^posts/archive/(?P<y>[0-9]{4})/(?P<m>[0-9]{1,2})$', post_list_by_ym, name='list_by_ym'),
	url(r'^posts/tag/(?P<tag>\w+)$', post_list_by_tag, name='list_by_tag'),
	url(r'^search/$',views.blog_search, name = "blog_search"),#按文章标题搜索
	
	
	
)