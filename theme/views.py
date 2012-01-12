from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils import simplejson

from django.contrib import messages

from domain.models import *
from theme.models import *

def list(request):
    themes = Theme.objects.all()
    return render_to_response('theme/theme_list.html', locals(), context_instance=RequestContext(request))

