import zipfile

from django import forms
from django.utils.translation import ugettext as _

from .utils import connect_aws_s3, create_bucket, push_file_to_s3


class UploadForm(forms.Form):
    bucket_name = forms.CharField(max_length=255, required=True, help_text=_(u'Please select a unicode bucket_name.'))
    zip_file = forms.FileField(required=True, help_text=_(u'The zip file contain all files of a static web site.'))

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

        if not zipfile.is_zipfile(zip_file):
            raise forms.ValidationError(_(u'%s is not a valid zip file.' % zip_file.name))

        return zip_file

