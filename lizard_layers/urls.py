# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf import settings

from django.conf.urls.defaults import url
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns

from django.contrib import admin

from lizard_layers.views import GeoserverLayer
from lizard_layers.views import SecureGeoserverView
from lizard_layers.views import AreaValueView


API_URL_NAME = 'lizard_layers_api_root'


admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^admin/', include(admin.site.urls)),
    url(r'^wms/$',
      GeoserverLayer.as_view(),
      {},
      'lizard_layers.geoserver_view'),
    url(r'^secure/wms/$',
      SecureGeoserverView.as_view(),
      {},
      'lizard_layers.secure_geoserver_view'),
    url(r'^value/$',
      AreaValueView.as_view(),
      {},
      'lizard_layers.area_value_view'),
    (r'^api/',
     include('lizard_layers.api.urls')),
    )


if settings.DEBUG:
    # Add this also to the projects that use this application
    urlpatterns += patterns('',
        (r'', include('staticfiles.urls')),
    )


def handler500(request):
    """
    500 error handler which includes ``request`` in the context.

    Templates: `500.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template(
        '500.html'
    )  # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))
