from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
	url(r'', include('zone.urls')),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
	url(r'^search/', include('haystack.urls')),
	url(r'^comments/', include('django_comments.urls')),
	url(r'^user_register/',"zone.views.user_register", name="user_register"),
	#url(r'^archive/$','zone.views.archive',name="archive"),
	
)