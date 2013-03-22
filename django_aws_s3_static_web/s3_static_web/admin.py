from django.contrib import admin

from .models import StaticWebBucket


class StaticWebBucketAdmin(admin.ModelAdmin):
    list_display = (
    'user', 'title', 'bucket_name', 'index_html', 'error_html', 'is_public_this_site', 'is_s3_public', 'created')


admin.site.register(StaticWebBucket, StaticWebBucketAdmin)