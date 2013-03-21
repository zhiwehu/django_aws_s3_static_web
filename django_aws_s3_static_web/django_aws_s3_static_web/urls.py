from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='base.html'), name='home'),

    # Examples:
    # url(r'^$', 'django_aws_s3_static_web.views.home', name='home'),
    # url(r'^django_aws_s3_static_web/', include('django_aws_s3_static_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^s3/', include('s3_static_web.urls')),

    url(r'^accounts/', include('allauth.urls')),
)
