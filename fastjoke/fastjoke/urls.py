from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'', include('jokeFeed.urls', namespace='jokeFeed')),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login', {}),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page' : '/'}),
	url(r'^accounts/add$', 'jokeFeed.views.add_user', name='add_user'),
	url(r'^accounts/add/add$', 'jokeFeed.views.add_user_add', name='add_user_add'),
    # Examples:
    # url(r'^$', 'fastjoke.views.home', name='home'),
    # url(r'^fastjoke/', include('fastjoke.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
