# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

# Create your views here.
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from urllib2 import urlopen
from urllib import quote


class GeoserverLayer(View):
    """
    Pass layer request to geoserver and return result

    Meanwhile, add cql filter corresponding to lizard-security rights
    and corresponding to amount of layers requested.
    
        >>> from lizard_layers.views import GeoserverLayer
        >>> gl = GeoserverLayer()

        >>> gl._quoted_get_par('SOME_PAR', 'bla bla')
        '&SOME_PAR=bla%20bla'
    """

    def _multiply_cql_filter(self, cql_filter, amount):
        """
        Return string of repeated cql amount times with ';' as separator.
        """
        return ';'.join([cql_filter for i in range(amount)])

    def _quoted_get_par(self, name, value):
        """
        Return get parameter as string with value quoted.
        """
        return '&' + name + '=' + quote(value)

    def _id_set_to_cql(self, id_set):
        """
        Convert id_set to cql section.
        """
        str_ids = [str(i) for i in id_set]
        csv_ids = ','.join(str_ids)
        cql = 'data_set_id in (%s)' % csv_ids

        return cql

    def _amount_of_layers(self, request):
        """
        Return amount of wms layers requested.
        """
        return len(request.GET.get('LAYERS').split(','))

    def _get_pars(self, request):
        """
        Return get_pars as string from request.
        """
        return request.get_full_path().split('?')[-1]

    def _amount_of_layers(self, request):
        """
        Return amount of wms layers requested.
        """
        return len(request.GET.get('LAYERS').split(','))

    def _request_to_cql_filter(self, request):
        """
        Build cql_filter based on session user and data_set rights.

        Assumes lizard_security.
        """
        # Super users get no filtering
        if request.user is not None and request.user.is_superuser:
            return None
        # Normal users get filtering according to allowed_data_set_ids
        if request.allowed_data_set_ids:
            return (self._id_set_to_cql(request.allowed_data_set_ids) +
                   ' or data_set_id is null')
        # Others only see objects without a data_set
        return 'data_set_id is null'

    def _geoserver_url(self, request):
        """
        Return geoserver url.
        """

        get_pars = self._get_pars(request)
        cql_filter = self._request_to_cql_filter(request)

        if cql_filter is None:
            return (settings.GEOSERVER_URL +
                    '?' + get_pars)

        # If there are more layers, we need more filters
        cql_filters = self._multiply_cql_filter(
            cql_filter,
            self._amount_of_layers(request),
        )

        # The filter part must be quoted
        cql_par = self._quoted_get_par(
            'CQL_FILTER', cql_filters
        )
        print cql_filters

        return (settings.GEOSERVER_URL +
                '?' + self._get_pars(request) +
                cql_par)
        
    def _url_to_response(self, url):
        """
        Return django response object retrieved from remote url.
        """
        urlopen_object = urlopen(url)
        content = urlopen_object.read()
        content_type = urlopen_object.headers['content-type']

        response = HttpResponse(
            content,
            content_type=content_type,
        )
        return response

    def get(self, request, *args, **kwargs):
        """
        Return layer from geoserver applying security filter.
        """
        url = self._geoserver_url(request)
        print url
        return self._url_to_response(url)
