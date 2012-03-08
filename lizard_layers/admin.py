from django.contrib import admin

from lizard_layers.models import ValueType
from lizard_layers.models import AreaValue
from lizard_layers.models import ParameterType


class ValueTypeAdmin(admin.ModelAdmin):
    list_display_links = ['name']
    list_display = [
        'name',
    ]


class AreaValueAdmin(admin.ModelAdmin):
    list_display_links = ['area']
    list_display = [
        'area',
        'value',
        'value_type',
    ]


class ParameterTypeAdmin(admin.ModelAdmin):
    list_display_links = ['value_type']
    list_display = [
        'value_type',
        'parameter',
    ]


admin.site.register(ParameterType, ParameterTypeAdmin)
admin.site.register(ValueType, ValueTypeAdmin)
admin.site.register(AreaValue, AreaValueAdmin)
