# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.core.mail import send_mail

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


from domain.models import *
from domain.forms import *

import datetime, random, sha

import settings

# ========================
# Utility Functions
# ========================

# Validate all step function form URl and query
def validate(request, validate_package=False):
    error = False

    domain_prefix = request.POST.get('domain') or request.GET.get('domain') or ''
    if not domain_prefix:
        messages.error(request, _('Please include website name.'))
        error = True
    else:
        if Site.objects.filter(name=domain_prefix).count():
            messages.error(request, _('Your website name already exist.'))
            error = True
        if len(domain_prefix) > 128:
            messages.error(request, _('Your website name must be shorter than 128 character.'))
            error = True
        # TODO: Check if domain name isn't URL format

    if validate_package:
        package_code = request.POST.get('package') or request.GET.get('package') or ''
        if not package_code:
            messages.error(request, _('Please select package.'))
            error = True
        else:
            if not Package.objects.filter(code=package_code).count():
                messages.error(request, _('Your package not match.'))
                error = True

    return not error

# Add new site for status QUEUE
def create_site(request):
    package = Package.objects.get(code=request.POST.get('package'))
    Site.objects.create(
        name=request.POST.get('domain'),
        system=package.system,
        status=Site.QUEUE,
        package=package,
        user=request.user
    )

# ========================
# Access from urls.py
# ========================
def home(request):
    error = request.GET.get('error')
    domain_prefix = request.GET.get('domain') or ''
    domain_suffix =  settings.OW_DOMAIN

    return render_to_response('domain/home.html', locals(), context_instance=RequestContext(request))

def packages(request):
    error = request.GET.get('error')
    domain_prefix = request.GET.get('domain') or ''
    if not validate(request): return HttpResponseRedirect('/?error=1&domain=%s' % domain_prefix)

    domain_suffix =  settings.OW_DOMAIN
    packages = Package.objects.all()
    return render_to_response('domain/packages.html', locals(), context_instance=RequestContext(request))

def register(request):
    if request.user.is_authenticated():
            raise Http404

    if request.POST:
        form = RegistrationForm(request.POST) 
        if form.is_valid():
            username = form.cleaned_data['username']
            email    = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user = User.objects.create_user(username, email, password)
            user.is_active = False
            user.save()

            user = authenticate(username=username, password=password)
            login(request, user)

            messages.info(request, _('Validate account on your email.'))
            if request.POST.get('domain') and request.POST.get('package'):
                # run script build site
                create_site(request)
                return HttpResponseRedirect('/build/%s' % request.POST.get('domain'))
            print request.path
            return HttpResponseRedirect('/')
        else:
            messages.error(request, _('Register error'))
            if request.POST.get('domain') and request.POST.get('package'):
                return auth(request, True)
    else:
        form = RegistrationForm()

    register_form = form

    return render_to_response('domain/register.html', locals(), context_instance=RequestContext(request))

def sign_in(request):
    if request.user.is_authenticated():
            raise Http404

    if request.POST:
        form = SignInForm(request.POST) 
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if request.POST.get('domain') and request.POST.get('package'):
                    # run script build site
                    create_site(request)
                    return HttpResponseRedirect('/build/%s' % request.POST.get('domain'))
                return HttpResponseRedirect('/')
            else:
                messages.error(request, _('Username or password miss match'))
                if request.POST.get('domain') and request.POST.get('package'):
                    return auth(request, True)

    else:
        form = SignInForm()

    sign_in_form = form

    return render_to_response('domain/sign_in.html', locals(), context_instance=RequestContext(request))

def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/')

def auth(request, error=False):
    domain_prefix = request.POST.get('domain') or request.GET.get('domain') or ''
    package_code = request.POST.get('package') or request.GET.get('package') or ''
    if not validate(request, True): return HttpResponseRedirect('/packages/?error=1&domain=%s&package=%s' % (domain_prefix, package_code))

    domain_suffix =  settings.OW_DOMAIN
    package = Package.objects.get(code=package_code)

    register_form = RegistrationForm()
    sign_in_form = SignInForm()

    if request.POST:
        if request.POST.get('callback') == 'sign_in':
            sign_in_form = SignInForm(request.POST)
        elif request.POST.get('callback') == 'register':
            register_form = RegistrationForm(request.POST)
        if not error:
            return eval('%s(request)' % request.POST.get('callback'))

    return render_to_response('domain/auth.html', locals(), context_instance=RequestContext(request))
    
def build(request, site_name=None):
    if request.user.is_authenticated():
        if request.POST.get('domain') and request.POST.get('package'):
            # run script build site
            create_site(request)
            return HttpResponseRedirect('/build/%s' % request.POST.get('domain'))
        try:
            domain_suffix =  settings.OW_DOMAIN
            site = Site.objects.get(name=site_name)
            return render_to_response('domain/build.html', locals(), context_instance=RequestContext(request))
        except Site.DoesNotExist:
            raise Http404

    return auth(request)
    
def get_site_percent(request, site_name):
        try:
            return HttpResponse(simplejson.dumps({'percent': Site.objects.get(name=site_name).percent}), mimetype='application/javascript')
        except Site.DoesNotExist:
            raise Http404
