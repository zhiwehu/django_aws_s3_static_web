from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^upload/$', 's3_static_web.views.upload', name='upload'),
)
