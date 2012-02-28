# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

# Create your views here.
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from urllib2 import urlopen
from urllib import urlencode


class GeoserverLayer(View):
    """
    Pass layer request to geoserver and return result

    Meanwhile, add cql filter corresponding to lizard-security rights
    and corresponding to amount of layers requested.

        >>> from lizard_layers.views import GeoserverLayer
        >>> gl = GeoserverLayer()

        >>> gl._id_set_to_cql(id_set=set([1, 3]))
        'data_set_id in (1,3)'
    """

    def _id_set_to_cql(self, id_set):
        """
        Convert id_set to cql section.
        """
        str_ids = [str(i) for i in id_set]
        csv_ids = ','.join(str_ids)
        cql = 'data_set_id in (%s)' % csv_ids

        return cql

    def _multiply_cql_filter(self, cql_filter, amount):
        """
        Return string of repeated cql amount times with ';' as separator.
        """
        if not cql_filter:
            return ''

        return ';'.join([cql_filter for i in range(amount)])

    def _security_cql(self, request):
        """
        Build cql_filter based on session user and data_set rights.

        Assumes lizard_security.
        """
        # Super users get no filtering
        if request.user is not None and request.user.is_superuser:
            return None
        # Normal users get filtering according to allowed_data_set_ids
        if request.allowed_data_set_ids:
            return ('(' +
                    self._id_set_to_cql(request.allowed_data_set_ids) +
                   ' or data_set_id is null)')
        # Others only see objects without a data_set
        return 'data_set_id is null'

    def _query_dict_to_dict(self, query_dict):
        """
        Return a normal dict.

        
        """


    def _geoserver_url(self, request):
        """
        Return geoserver url, extending existing cql filters with
        with security related cql parameters based on request user.
        """
        GET = request.GET.copy()

        # Don't trust the case layers and cql_filter is in.
        layer_keys = [k for k in GET if k.lower() == 'layers']
        cql_keys = [k for k in GET if k.lower() == 'cql_filter']

        cql_filter_parts = [self._security_cql(request)]

        if cql_keys:
            # If cql_filter is a ';'-separated list, take only the first
            cql_filter_parts.extend([f.split(';')[0]
                                     for k in cql_keys
                                     for f in GET.pop(k)])

        cql_filter = ' and '.join(filter(bool, cql_filter_parts))

        # If there are more layers, we need more filters
        amount_of_layers = sum(
            [len(GET[k].split(',')) for k in layer_keys],
        )

        cql_filters = self._multiply_cql_filter(
            cql_filter=cql_filter,
            amount=amount_of_layers,
        )

        if cql_filters:
            GET.update(dict(cql_filter=cql_filters))


        print
        print GET.urlencode()
        print

        return settings.GEOSERVER_URL + '?' + GET.urlencode()

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
        return self._url_to_response(url)
