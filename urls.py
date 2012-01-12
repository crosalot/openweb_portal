from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # domain:
    url(r'^$', 'domain.views.home', name='home'),
    url(r'^packages/$', 'domain.views.packages', name='packages'),
    url(r'^build/$', 'domain.views.build', name='build'),
    url(r'^build/(?P<site_name>\w+)/$', 'domain.views.build', name='build_status'),
    url(r'^register/$', 'domain.views.register', name='register'),
    url(r'^sign-in/$', 'domain.views.sign_in', name='sign_in'),
    url(r'^sign-out/$', 'domain.views.sign_out', name='sign_out'),
    url(r'^ajax/get/site-percent/(?P<site_name>\w+)/$', 'domain.views.get_site_percent', name='get_site_percent'),

    #theme
    url(r'^themes/$', 'theme.views.list', name='theme_list'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls'))
    ) + urlpatterns
