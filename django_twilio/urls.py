# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^(?P<twiml_name>[\w-]+)/$',
        'django_twilio.views.twiml_detail'),
    url(r'^(?P<twiml_id>\d+)/$',
        'django_twilio.views.twiml_detail_id'),)
