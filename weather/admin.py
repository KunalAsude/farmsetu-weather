from django.contrib import admin
from .models import WeatherRegion, WeatherParameter, WeatherData, DataSource

@admin.register(WeatherRegion)
class WeatherRegionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'description']
    search_fields = ['code', 'name']

@admin.register(WeatherParameter)
class WeatherParameterAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'unit']
    search_fields = ['code', 'name']

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['region', 'parameter', 'year', 'month', 'value', 'created_at']
    list_filter = ['region', 'parameter', 'year']
    search_fields = ['region__code', 'parameter__code']
    date_hierarchy = 'created_at'
    ordering = ['-year', '-month']

@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ['region', 'parameter', 'last_updated', 'is_active']
    list_filter = ['is_active', 'last_updated']
    search_fields = ['region__code', 'parameter__code']