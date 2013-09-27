from django.conf.urls import patterns,  url



urlpatterns = patterns('jokeFeed.views',
	url(r'^$', 'index', name='index'),
	url(r'^submit$', 'submit', name='submit'),
	url(r'^submit/submit$', 'submit_submit', name='submit_submit'),
	url(r'^(?P<joke_id>\d+)/$', 'detail', name='detail'),
	url(r'^(?P<joke_id>\d+)/up/$', 'up', name='up'),
	url(r'^(?P<joke_id>\d+)/down/$', 'down', name='down'),
	
    # Examples:
    # url(r'^$', 'kit.views.home', name='home'),
    # url(r'^kit/', include('kit.foo.urls')),
)
