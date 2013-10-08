from django.conf.urls import patterns,  url



urlpatterns = patterns('jokeFeed.views',
	url(r'^$', 'index', name='index'),
	url(r'^submit$', 'submit', name='submit'),
	url(r'^submit/submit$', 'submit_submit', name='submit_submit'),
	url(r'^(?P<joke_id>\d+)/$', 'detail', name='detail'),
	url(r'^(?P<joke_id>\d+)/up/$', 'up', name='up'),
	url(r'^(?P<joke_id>\d+)/down/$', 'down', name='down'),
	url(r'^(?P<joke_id>\d+)/fav/$', 'fav', name='fav'),
	url(r'^user/fav$', 'view_fav', name='user_fav'),
	url(r'^user/profile$', 'view_profile', name='user_profile'),
	
    # Examples:
    # url(r'^$', 'kit.views.home', name='home'),
    # url(r'^kit/', include('kit.foo.urls')),
)
