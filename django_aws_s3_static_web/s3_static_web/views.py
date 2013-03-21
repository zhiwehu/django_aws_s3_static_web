from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from .forms import UploadForm
from .utils import upload_zip_file_s3


@login_required
def upload(request, template='s3_static_web/upload.html', extra_context=None):
    upload_form = UploadForm()
    if request.method == 'POST':
        upload_form = UploadForm(data=request.POST, files=request.FILES)
        if upload_form.is_valid():
            bucket = upload_form.bucket
            zipped_file = upload_form.cleaned_data['zip_file']
            index_html = upload_form.cleaned_data.get('index_html', 'index.html')
            error_html = upload_form.cleaned_data.get('error_html', 'error.html')
            upload_zip_file_s3(bucket, zipped_file)
            bucket.configure_website(index_html, error_html)
            website_url = bucket.get_website_endpoint()
            context = {
                'website_url': website_url,
            }
            if extra_context:
                context.update(extra_context)
            return render_to_response('s3_static_web/upload_success.html', context,
                                      context_instance=RequestContext(request))

    context = {
        'upload_form': upload_form,
    }
    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))
