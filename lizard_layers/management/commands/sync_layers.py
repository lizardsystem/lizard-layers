#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from optparse import make_option

from django.core.management.base import BaseCommand
from lizard_fewsnorm.models import FewsNormSource

from lizard_area.models import Area
from lizard_layers.models import AreaValue
from lizard_layers.models import ValueType

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Synchronizes trackrecords in datasources into TrackRecordCache.
    """
    def handle(self, *args, **options):
        for value_type in ValueType.objects.all():
            for area in Area.objects.filter(
                area_class=Area.AREA_CLASS_KRW_WATERLICHAAM,
            ):
                from random import random
                area_value, created = AreaValue.objects.get_or_create(
                    value_type=value_type,
                    area=area
                )
                area_value.value = random()
                area_value.save()
