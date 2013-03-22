import zipfile

from django import forms
from django.utils.translation import ugettext as _

from .models import StaticWebBucket
from .settings import MAX_ZIP_FILE_SIZE
from .utils import connect_aws_s3, create_bucket


class StaticWebForm(forms.ModelForm):
    class Meta:
        model = StaticWebBucket
        fields = ('title', 'bucket_name', 'zip_file', 'index_html', 'error_html', 'is_s3_public', 'is_public_this_site')

    def clean_bucket_name(self):
        bucket_name = self.cleaned_data['bucket_name']
        try:
            conn = connect_aws_s3()
            self.bucket = create_bucket(conn, bucket_name)
        except Exception as e:
            raise forms.ValidationError(_(u'Got errors: %s' % e))
        return bucket_name

    def clean_zip_file(self):
        zip_file = self.cleaned_data['zip_file']

        if zip_file.size > MAX_ZIP_FILE_SIZE:
            raise forms.ValidationError(_(u'%s size should be less than %d, current is %d' % (zip_file.name, MAX_ZIP_FILE_SIZE, zip_file.size)))

        if not zipfile.is_zipfile(zip_file):
            raise forms.ValidationError(_(u'%s is not a valid zip file.' % zip_file.name))

        return zip_file

