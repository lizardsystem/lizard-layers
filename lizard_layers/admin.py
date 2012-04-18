from django.contrib import admin

from lizard_layers.models import (
    ValueType,
    AreaValue,
    ParameterType,
    ServerMapping,
)


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
        'flag',
        'comment',
        'value_type',
    ]


class ParameterTypeAdmin(admin.ModelAdmin):
    list_display_links = ['value_type']
    list_display = [
        'value_type',
        'measuring_rod_code',
        'parameter',
    ]

admin.site.register(ParameterType, ParameterTypeAdmin)
admin.site.register(ValueType, ValueTypeAdmin)
admin.site.register(AreaValue, AreaValueAdmin)
admin.site.register(ServerMapping)
