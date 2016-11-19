from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import RegisterView
from zone.views import myacticles
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
	url(r'', include('zone.urls')),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
	url(r'^search/', include('haystack.urls')),
	url(r'^comments/', include('django_comments.urls')),
	url(r'^register/$', RegisterView.as_view(), name='register'),
	url(r'^myacticles/$','zone.views.myacticles',name="myacticles"),
	url(r'^About me/$','zone.views.About_me',name="About_me"),
	#url(r'^archive/$','zone.views.archive',name="archive"),
	
)