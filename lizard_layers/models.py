# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# from django.db import models

# Create your models here.

from django.utils.translation import ugettext as _
from django.contrib.gis.db import models
from lizard_area.models import Area
from lizard_fewsnorm.models import ParameterCache
from lizard_measure.models import MeasuringRod

class ValueType(models.Model):
    """
    Value type.
    """
    name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name=_('Name'),
    )

    class Meta:
        verbose_name = _('Value type')
        verbose_name_plural = _('Value types')

    def __unicode__(self):
        return self.name


class AreaValue(models.Model):
    """
    Relates a value to an area for drawing with geoserver.
    """
    area = models.ForeignKey(
        Area,
        null=True,
        blank=True,
        verbose_name=_('Area'),
    )

    value_type = models.ForeignKey(
        ValueType,
        null=True,
        blank=True,
        verbose_name=_('Value type'),
    )
    
    value = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Value'),
    )

    class Meta:
        verbose_name = _('Area value')
        verbose_name_plural = _('Area values')

    def __unicode__(self):
        return '%s - %s' % (self.area, self.value)


class ParameterType(models.Model):
    """
    Parameter type. To connect fewsparameters to geoserver layers.
    """
    value_type = models.ForeignKey(
        ValueType,
        null=True,
        blank=True,
        verbose_name=_('Value type'),
    )
    parameter = models.ForeignKey(
        ParameterCache,
        null=True,
        blank=True,
        verbose_name=_('Parameter'),
    )
    measuring_rod = models.ForeignKey(
        MeasuringRod,
        null=True,
        blank=True,
        verbose_name=_('MeasuringRod'),
    )

    class Meta:
        verbose_name = _('Parameter type')
        verbose_name_plural = _('Parameter types')

    def __unicode__(self):
        return '%s - %s' % (self.value_type.name, self.parameter)
