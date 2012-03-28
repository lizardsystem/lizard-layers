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
from lizard_measure.models import MeasuringRod
from lizard_measure.models import Score

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Synchronizes ESF and EKR in datasources into cache table.
    """
    def update_area_value(self, area, value, value_type, flag=None, comment=None):
        area_value, created = AreaValue.objects.get_or_create(
            area=area,
            value_type=value_type,
        )
        area_value.value = value
        area_value.flag = flag
        area_value.comment = comment
        area_value.save()
        return created

    def _judgements(self, values, area):
        """
        Calculate individual judgements.
        """
        judgements = []
        for value in values:
            # TODO Performance improvement possible here.
            try:
                score = Score.objects.get(
                    measuring_rod=value['parameter_type'].measuring_rod,
                    area=area,
                )
                judgements.append(
                    score.judgement(
                        value['value'],
                        score.target_2015,
                    )
                )
            except Score.DoesNotExist:
                judgements.append(None)
        return judgements

    def _overall_judgement(self, judgements):
        """
        Return overall judgement.
        """
        if None in judgements:
            return None
        if (min(judgements) == 1 and
            len([j for j in judgements if j > 1]) >= 2):
            return 2
        if (min(judgements) == 1 and
            len([j for j in judgements if j > 1]) < 2):
            return 1
        if len([j for j in judgements if j < 1]) == 1:
            return -1
        if len([j for j in judgements if j < 1]) > 1:
            return -2

    def sync_ekr(self):
        value_type_worst = ValueType.objects.get(name='EKR-ONGUNSTIG')
        value_type_score = ValueType.objects.get(name='EKR-DOELSCORE')

        parameter_types = list(ParameterType.objects.all())

        for area in Area.objects.filter(
            area_class=Area.AREA_CLASS_KRW_WATERLICHAAM,
        ):

            values = []
            for parameter_type in parameter_types:
                timeseries = TimeSeriesCache.objects.filter(
                    parametercache=parameter_type.parameter,
                    geolocationcache__ident=area.ident,
                )
                value = None
                flag = None
                comment = None
                if timeseries:
                    timeserie = timeseries[0]
                    try:
                        event = timeserie.get_latest_event(with_comments=True)
                        value = event.value
                        flag = event.flag
                        comment = event.comment
                    except IndexError:
                        # No events at all
                        pass

                self.update_area_value(
                    area=area,
                    value=value,
                    flag=flag,
                    comment=comment,
                    value_type=parameter_type.value_type,
                )
                values.append({
                    'parameter_type': parameter_type,
                    'value': value
                })

            try:
                value_worst = min([v['value'] for v in values
                                   if v['value'] is not None])
            except ValueError:
                # All ekrs are None
                value_worst = None

            self.update_area_value(
                area=area,
                value=value_worst,
                value_type=value_type_worst,
            )
            judgements = self._judgements(values, area)
            overall_judgement = self._overall_judgement(judgements)
            self.update_area_value(
                area=area,
                value=overall_judgement,
                value_type=value_type_score,
            )

    def sync_esf(self):
        pass

    def handle(self, *args, **options):
       self.sync_ekr()
       self.sync_esf()
