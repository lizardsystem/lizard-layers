from django.contrib import admin

from lizard_layers.models import ValueType
from lizard_layers.models import AreaValue


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


admin.site.register(ValueType, ValueTypeAdmin)
admin.site.register(AreaValue, AreaValueAdmin)
