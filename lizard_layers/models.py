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
    timestamp = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Timestamp'),
    )

    class Meta:
        verbose_name = _('Area value')
        verbose_name_plural = _('Area values')

    def __unicode__(self):
        return '%s - %s/%s' % (self.area, self.value, self.comment)

    @classmethod
    def _table_value_types(cls, use_value_types=None):
        # make a dict of value_types, by name
        if use_value_types:
            value_types = dict(
                [(vt.name, vt) for vt in
                 ValueType.objects.filter(name__in=use_value_types)])
        else:
            value_types = dict(
                [(vt.name, vt) for vt in ValueType.objects.all()])
        return value_types

    @classmethod
    def table_header(cls, use_value_types=None):
        """Get table header, for use with as_table"""
        result = ['Locatie', ]
        if use_value_types:
            result.extend(use_value_types)
        else:
            result.extend(cls._table_value_types().keys())
        return result

    @classmethod
    def as_table(cls, use_value_types=None, add_header=False):
        """
        How contents as table (list of lists).

        It shows krw waterlichamen per row and valuetypes as columns.

        options:
        use_value_types: only display these value types
        as_ekr: display custom

        Initial version of function.
        """
        value_types = cls._table_value_types(use_value_types=use_value_types)
        # use_value_types makes the order of the items
        if not use_value_types:
            use_value_types = value_types.keys()

        areas = Area.objects.exclude(name=None).filter(
            area_class=Area.AREA_CLASS_KRW_WATERLICHAAM)
        area_values = dict([
                ((area_value.area.ident, area_value.value_type.name), area_value)
                for area_value in cls.objects.filter(area__in=areas)])

        result = []
        if add_header:
            # First row is the header
            result.append(cls.table_header(use_value_types=use_value_types))

        for area in areas:
            # Each row starts with an area name plus all values
            row = [area.name]
            for value_type_name in use_value_types:
                area_value = area_values.get((area.ident, value_type_name), None)
                if area_value is not None:
                    row.append(area_value)
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
