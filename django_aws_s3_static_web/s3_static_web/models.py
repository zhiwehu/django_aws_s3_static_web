import os

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from model_utils.models import TimeStampedModel

from .utils import upload_zip_file_s3, get_random_filename, connect_aws_s3

try:
    from PIL import Image

    dir(Image) # Placate PyFlakes
except ImportError:
    import Image


def thumbnail_upload_to(instance, filename):
    filename = get_random_filename(filename)
    path = '%s/%s/' % (instance.user.username, instance.title)
    return os.path.join(path, filename)


def zip_file_upload_to(instance, filename):
    path = '%s/%s/' % (instance.user.username, instance.title)
    return os.path.join(path, filename)


class StaticWebBucket(TimeStampedModel):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255, verbose_name=_(u'Site Title'))
    bucket_name = models.CharField(max_length=255, verbose_name=_(u' S3 Bucket Name'),
                                   help_text=_(u'A unique bucket name in AWS S3.'))
    index_html = models.CharField(max_length=255, verbose_name=_(u'Index html'), null=True, blank=True)
    error_html = models.CharField(max_length=255, verbose_name=_(u'Error html'), null=True, blank=True)
    zip_file = models.FileField(help_text=_(u'The zip file contains all files of a static web site.'),
                                upload_to=zip_file_upload_to)
    thumbnail = models.ImageField(upload_to=thumbnail_upload_to, null=True, blank=True)
    website_endpoint = models.URLField(verbose_name=_(u'Website Endpoint'), null=True, blank=True)
    is_public_this_site = models.BooleanField(verbose_name=_(u'Is public for this site ?'), default=True,
                                              help_text=_(u'Not valid if not public in AWS S3.'))
    is_s3_public = models.BooleanField(verbose_name=_(u'Is public in AWS S3 ?'), default=True)

    def __unicode__(self):
        return self.title

    def upload_zip_s3(self, bucket):
        result = {'errors': []}
        try:
            upload_zip_file_s3(bucket, self.zip_file)
        except Exception as e:
            result['errors'].append(e.error_message)
        if self.index_html:
            try:
                bucket.configure_website(suffix=self.index_html)
            except Exception as e:
                result['errors'].append(e.error_message)
        if self.error_html:
            try:
                bucket.configure_website(error_key=self.error_html)
            except Exception as e:
                result['errors'].append(e.error_message)
        self.website_endpoint = bucket.get_website_endpoint()
        return result

    def remove_bucket(self):
        conn = connect_aws_s3()
        bucket = conn.get_bucket(self.bucket_name)
        for key in bucket.list():
            key.delete()
        conn.delete_bucket(bucket)
        pass

    def save(self, *args, **kwargs):
        if not self.is_s3_public:
            self.is_public_this_site = False
        super(StaticWebBucket, self).save(*args, **kwargs)
