#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from optparse import make_option

from django.core.management.base import BaseCommand
from lizard_fewsnorm.models import FewsNormSource

from lizard_area.models import Area
from lizard_layers.models import AreaValue
from lizard_layers.models import ValueType
from lizard_layers.models import ParameterType
from lizard_fewsnorm.models import TimeSeriesCache

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Synchronizes ESF and EKR in datasources into cache table.
    """
    def update_area_value(self, area, value, value_type):
        area_value, created = AreaValue.objects.get_or_create(
            area=area,
            value_type=value_type,
        )
        area_value.value = value
        area_value.save()
        return created

    def calculate_value_score(self, values):
        return None  # TODO
        
    def sync_ekr(self):
        value_type_worst = ValueType.objects.get(name='EKR-ONGUNSTIG')
        value_type_score = ValueType.objects.get(name='EKR-DOELSCORE')
       
        parameter_types = list(ParameterType.objects.all())

        for area in Area.objects.filter(
            area_class=Area.AREA_CLASS_KRW_WATERLICHAAM,
        ):

            values = {}
            for parameter_type in parameter_types:
                timeseries = TimeSeriesCache.objects.filter(
                    parametercache=parameter_type.parameter,
                    geolocationcache__ident=area.ident,
                )
                if timeseries:
                    timeserie = timeseries[0]
                    try:
                        value = timeserie.get_latest_event().value
                    except IndexError:
                        value = None
                else: value = None
                self.update_area_value(
                    area=area,
                    value=value,
                    value_type=parameter_type.value_type,
                )
                values.update({parameter_type.value_type: value})
            
            try:
                value_worst = min([v for v in values.values()
                                   if values is not None])
            except ValueError:
                # All ekrs are None
                value_worst = None

            self.update_area_value(
                area=area,
                value=value_worst,
                value_type=value_type_worst,
            )
            value_score = self.calculate_value_score(values)
            self.update_area_value(
                area=area,
                value=value_score,
                value_type=value_type_score,
            )

    def sync_esf(self):
        pass

    def handle(self, *args, **options):
       self.sync_ekr()
       self.sync_esf()
       #for parameter_type in ValueType.objects.all():
           
               #from random import random
               #area_value, created = AreaValue.objects.get_or_create(
                   #value_type=value_type,
                   #area=area
               #)
               #area_value.value = random()
               #area_value.save()
        # for fewsnormsource in fewsnormsources
        
        # if location present with ident = area ident
            # for parameter in ekrpars
                # if parameter in cache
                    # get latest before deadline
                    # save area value
            # calculate accumulation
                # save accumulation
            # 
           

