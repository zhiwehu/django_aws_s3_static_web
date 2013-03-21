from StringIO import StringIO

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from .forms import UploadForm
from .utils import fileiterator, push_file_to_s3

@login_required
def upload(request, template='s3_static_web/upload.html', extra_context=None):
    upload_form = UploadForm()
    if request.method == 'POST':
        upload_form = UploadForm(data=request.POST, files=request.FILES)
        if upload_form.is_valid():
            bucket = upload_form.bucket
            for filename, content in fileiterator(upload_form.cleaned_data['zip_file']):
                content_string = StringIO()
                content_string.write(content)
                push_file_to_s3(bucket, filename, content_string)

    context = {
        'upload_form': upload_form,
    }
    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))
