from django.conf.urls import patterns,  url



urlpatterns = patterns('jokeFeed.views',
	url(r'^$', 'index', name='index'),

	
    # Examples:
    # url(r'^$', 'kit.views.home', name='home'),
    # url(r'^kit/', include('kit.foo.urls')),
)
