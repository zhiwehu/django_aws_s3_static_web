from django.contrib.auth.decorators import login_required
from django.contrib.messages import success, error
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from .forms import StaticWebForm
from .models import StaticWebBucket


def home(request, template='s3_static_web/public_static_sites.html', extra_context=None):
    static_sites = StaticWebBucket.objects.filter(is_public_this_site=True)
    context = {
        'static_sites': static_sites,
    }
    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def static_site_post(request, static_site_id=None, template='s3_static_web/static_site_post.html', extra_context=None):
    static_site = None
    if static_site_id:
        action = _(u'Update')
        try:
            static_site = StaticWebBucket.objects.get(user=request.user, pk=static_site_id)
            form = StaticWebForm(instance=static_site)
        except:
            raise Http404
    else:
        action = _(u'Create')
        form = StaticWebForm(instance=static_site)

    if request.method == 'POST':
        form = StaticWebForm(data=request.POST, files=request.FILES, instance=static_site)
        if form.is_valid():
            bucket = form.bucket
            static_site = form.save(commit=False)
            static_site.user = request.user
            result = static_site.upload_zip_s3(bucket)
            if result.get('errors', None):
                for error in result['errors']:
                    error(request, error)
            static_site.save()
            return HttpResponseRedirect(reverse('static_site', args=[static_site.id, ]))

    context = {
        'form': form,
        'action': action,
    }
    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def user_static_sites(request, template='s3_static_web/user_static_sites.html', extra_context=None):
    static_sites = StaticWebBucket.objects.filter(user=request.user)
    context = {
        'static_sites': static_sites,
    }
    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def static_site(request, static_site_id, template='s3_static_web/static_site.html', extra_context=None):
    try:
        static_site = StaticWebBucket.objects.get(user=request.user, pk=static_site_id)
    except:
        raise Http404

    context = {
        'static_site': static_site,
    }
    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def delete_static_site(request, static_site_id):
    try:
        static_site = StaticWebBucket.objects.get(user=request.user, pk=static_site_id)
        static_site_title = static_site.title
    except:
        raise Http404

    try:
        static_site.remove_bucket()
    except Exception as e:
        error(request, e.error_message)
    static_site.delete()
    success(request, _(u'Delete %s successful.' % static_site_title))
    return HttpResponseRedirect(reverse('user_static_sites'))