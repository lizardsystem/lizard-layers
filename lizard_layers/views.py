# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

# Create your views here.
from django.conf import settings
from django.http import HttpResponse
from urllib2 import urlopen
from urllib import quote

def geoserver_layer(request):
        """
        Pass layer request to geoserver and return result
        """

        GEOSERVER_URL = settings.GEOSERVER_URL
        get_parameters = request.get_full_path().split('?')[-1]

        if request.user is not None and request.user.is_superuser:
            secure_get_parameters = get_parameters
        elif request.allowed_data_set_ids:
            id_list = '(' + ','.join(
                [str(i) for i in request.allowed_data_set_ids]
            ) + ')'
            cql_filter = ('data_set_id in %s' + 
                          ' or data_set_id is null') % id_list
            secure_get_parameters = get_parameters + '&CQL_FILTER=' + quote(cql_filter)
        else:
            cql_filter = ('data_set_id is null')
            secure_get_parameters = get_parameters + '&CQL_FILTER=' + quote(cql_filter)

        url = GEOSERVER_URL + '?' + secure_get_parameters

        geo = urlopen(url)
        content = geo.read()
        content_type = geo.headers['content-type']

        
        response = HttpResponse(
            content,
            content_type=content_type,
        )
        return response
