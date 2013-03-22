from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^$', 's3_static_web.views.home', name='home'),
                       url(r'^create/$', 's3_static_web.views.static_site_post', name='create_static_site'),
                       url(r'^(?P<static_site_id>\d+)/edit/$', 's3_static_web.views.static_site_post',
                           name='edit_static_site'),
                       url(r'^(?P<static_site_id>\d+)/$', 's3_static_web.views.static_site',
                           name='static_site'),
                       url(r'^(?P<static_site_id>\d+)/delete/$', 's3_static_web.views.delete_static_site',
                           name='delete_static_site'),
                       url(r'^my/$', 's3_static_web.views.user_static_sites', name='user_static_sites'),
)
