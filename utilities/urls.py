# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from utilities import settings

urlpatterns = patterns('',)

if settings.ENABLE_PASSWORD_RESET:
    urlpatterns += patterns('',
        (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
        (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete',
            {'template_name': 'admin/password_reset_complete.html'}),
    )
