import settings 
from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    url(r'^$', 'service.views.home'),
    url(r'login/$', 'service.views.login'),
    url(r'logout/$', 'service.views.logout'),
    url(r'test/$', 'service.views.test'),
    url(r'test/add/$', 'service.views.add_test'),
    url(r'test/(?P<test_id>\d+)/start/$', 'service.views.start_test'),
    url(r'test/(?P<test_id>\d+)/result/$', 'service.views.view_result'),
    url(r'^index/$', 'service.views.index'),
    url(r'^contact/$', 'service.views.contact'),
    url(r'^tools/$', 'service.views.tools'),
    url(r'^testing/$', 'service.views.testing'),
    url(r'^service/$', 'service.views.service'),
)
