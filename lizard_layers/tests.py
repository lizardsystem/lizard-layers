# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.test import TestCase
from lizard_layers.views import GeoserverLayer


class ExampleTest(TestCase):
    count = 0

    def setUp(self):
        self.gl = GeoserverLayer()

    def test_multiply_cql_filter(self):
        cql_filter = 'abc'
        amount = 3
        correct_result = 'abc;abc;abc'
        result = self.gl._multiply_cql_filter(cql_filter, amount)
        self.assertEquals(result, correct_result)

    def test_something(self):
        self.assertEquals(1, 1)
