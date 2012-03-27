from django.core.urlresolvers import reverse
from djangorestframework.views import View

from lizard_layers.models import ValueType
from lizard_layers.models import AreaValue
from lizard_api.base import BaseApiView
from lizard_area.models import Area


class RootView(View):
    """
    Startpoint.
    """
    def get(self, request):
        return {
            "value": reverse("lizard_layers_api_value"),
            }


class ValueView(View):
    """
    Return all Value/Area combinations in a 'table'.
    """

    def get(self, request):
        result = AreaValue.as_table()
        return result
