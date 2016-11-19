# coding=utf-8
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .commons import cache_manager
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse,render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Post,Page
from .forms import PostForm,UserForm
from haystack.forms import SearchForm
from datetime import datetime, timedelta
from django.template import RequestContext
import json


def first_page(request):
	return render(request,'zone/index.html',{})





def post_list(request):
	archives_db = Post.objects.filter(published_date__isnull=False)
	archives = []
	map_temp = {}
	for ar in archives_db:
		y = ar.published_date.year
		m = ar.published_date.month
		k = '{}|{}'.format(y, m)
		if k in map_temp:
			map_temp[k] += 1
		else:
			map_temp[k] = 1
	for kk,vv in map_temp.items():
		ym = kk.split('|')
		archives.append({'year':ym[0], 'month':ym[1], 'number': vv})
		
	postsAll = Post.objects.annotate(num_comment=Count('title')).filter(
		published_date__isnull=False).order_by('-published_date')
	paginator = Paginator(postsAll, 3)  # Show 5 contacts per page
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
        # If page is not an integer, deliver first page.
		posts = paginator.page(1)
	except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
		posts = paginator.page(paginator.num_pages)
	return render(request, 'zone/post_list.html', {'posts': posts, 'page': True,'ARCHIVES': archives,})
	
def post_detail(request,pk):
	post = get_object_or_404(Post,pk=pk)
	return render(request,'zone/post_detail.html',{'post':post} )

@login_required	
def post_new(request):
	if request.method == "POST":
		form =PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('zone.views.post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'zone/post_edit.html', {'form': form})
		

@login_required
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form =PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('zone.views.post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'zone/post_edit.html', {'form': form})
	
	
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    return render(request, 'zone/post_draft_list.html', {'posts': posts})
	

@login_required	
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('zone.views.post_detail', pk=pk)
	
	
	
	
def post_remove(request,pk):
	post = get_object_or_404(Post,pk=pk)
	post.delete()
	return redirect('zone.views.post_list')
	
	
def full_search(request):
	keywords = request.GET['q']
	sform = SearchForm(request.GET)
	posts = sform.search()
	return render(request, 'zone/post_search_list.html',
                  {'posts': posts, 'list_header': '关键字 \'{}\' 搜索结果'.format(keywords)})
				  
				  
def user_register(request):
	if request.method == "POST":
		uf = UserCreationForm(request.POST)
		if uf.is_valid():
            # #获取表单信息
			username = uf.cleaned_data['username']
			password1 = uf.cleaned_data['password1']
			password2 = uf.cleaned_data['password2']
            # #将表单写入数据库
			user = User()
			user.username = username
			user.password = password1
			user.save()
			print user.password
            # #返回注册成功页面
			return HttpResponse("Successy!")
	else:
		uf = UserCreationForm()
	return render_to_response('zone/register.html',{'uf':uf})
	
	
	




    
				  
def post_list_by_tag(request, tag):
    """根据标签列出已发布文章"""
    posts = Post.objects.annotate(num_comment=Count('comment')).filter(
        published_date__isnull=False, tags__name=tag).prefetch_related(
        'category').prefetch_related('tags').order_by('-published_date')
    for p in posts:
        p.click = cache_manager.get_click(p)
    return render(request, 'zone/post_list.html',
                  {'posts': posts, 'list_header': '文章标签 \'{}\''.format(tag)})
				  
def post_list_by_ym(request, y, m):
    """根据年月份列出已发布文章"""
    posts = Post.objects.annotate(num_comment=Count('title')).filter(
        published_date__isnull=False, published_date__year=y,
        published_date__month=m).prefetch_related(
        'category').prefetch_related('tags').order_by('-published_date')
    for p in posts:
        p.click = cache_manager.get_click(p)
    return render(request, 'zone/post_list.html',
                  {'posts': posts, 'list_header': '{0}年{1}月 的存档'.format(y, m)})

				  
def blog_search(request):#实现对文章标题的搜索
   
    is_search = True
    #ar_newpost = Article.objects.order_by('-publish_time')[:10]
    #classification = Classification.class_list.get_Class_list()    
    #tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    #date_list = Post.date_list.get_Article_onDate()

    error = False
    if 's' in request.GET:
        s = request.GET['s']
        if not s:
            return render(request,'zone/post_list.html')
        else:
            posts = Post.objects.filter(title__icontains = s)
            if len(posts) == 0 :
                error=True

    return render_to_response('zone/post_list.html',
            locals(),
            context_instance=RequestContext(request))

			
def myacticles(request):
	posts=Post.objects.all();
	return render(request,'zone/myacticles.html',{'posts':posts});
	
	
def About_me(request):
	return render(request,'zone/About_me.html',{});

















