# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# from django.db import models

# Create your models here.

from django.utils.translation import ugettext as _
from django.contrib.gis.db import models
from lizard_area.models import Area
from lizard_fewsnorm.models import ParameterCache
#from lizard_measure.models import MeasuringRod

class ServerMapping(models.Model):
    """
    Mapping between between external (geo)server and internal path.
    """
    name = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text=''
    )
    description = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text=''
    )
    description = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text=''
    )
    external_server = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text='Path to external geoserver not to be exposed to users'
    )
    relative_path = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text='Local path to be used by clients'
    )

    class Meta:
        verbose_name = _('Server mapping')
        verbose_name_plural = _('Server mappings')

    def __unicode__(self):
        return self.name


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
    flag = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Flag'),
    )
    comment = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name=_('Comment'),
    )

    class Meta:
        verbose_name = _('Area value')
        verbose_name_plural = _('Area values')

    def __unicode__(self):
        return '%s - %s' % (self.area, self.value)

    @classmethod
    def as_table(cls):
        """
        How contents as table (list of lists).

        Initial version of function.
        """
        areas = Area.objects.exclude(name=None).filter(
            area_class=Area.AREA_CLASS_KRW_WATERLICHAAM)
        area_values = dict([
                ((area_value.area.ident, area_value.value_type.name), area_value)
                for area_value in cls.objects.filter(area__in=areas)])
        value_types = ValueType.objects.all()

        result = []
        # First row is the header
        result.append(
            ['Locatie', ] +
            [value_type.name for value_type in value_types])
        for area in areas:
            # Each row starts with an area name plus all values
            row = [area.name]
            for value_type in value_types:
                area_value = area_values.get((area.ident, value_type.name), None)
                if area_value is not None and area_value.value is not None:
                    row.append(area_value.value)
                else:
                    row.append('-')
            result.append(row)
        return result


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
    # measuring_rod = models.ForeignKey(
    #     MeasuringRod,
    #     null=True,
    #     blank=True,
    #     verbose_name=_('MeasuringRod'),
    # )
    measuring_rod_code = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        verbose_name=_('MeasuringRodCode'),
    )

    class Meta:
        verbose_name = _('Parameter type')
        verbose_name_plural = _('Parameter types')

    def __unicode__(self):
        return '%s - %s' % (self.value_type.name, self.parameter)
