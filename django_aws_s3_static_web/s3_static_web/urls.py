from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^upload_static_zip/$', 's3_static_web.views.upload_static_zip', name='upload_static_zip'),
)
