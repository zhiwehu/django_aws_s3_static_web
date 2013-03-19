from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext


@login_required
def upload_static_zip(request, template='s3_static_web/upload_static_zip.html', extra_context=None):
    context = {}
    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))
