# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin

from lizard_layers.api.views import RootView
from lizard_layers.api.views import ValueView


admin.autodiscover()

NAME_PREFIX = 'lizard_layers_api_'


urlpatterns = patterns(
    '',
    url(r'^$',
        RootView.as_view(),
        name=NAME_PREFIX + 'root'),
    url(r'^value/$',
        ValueView.as_view(),
        name=NAME_PREFIX + 'value'),
    )
