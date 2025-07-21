from rest_framework import serializers
from .models import WeatherData, WeatherRegion, WeatherParameter, DataSource

class WeatherRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherRegion
        fields = '__all__'

class WeatherParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherParameter
        fields = '__all__'

class WeatherDataSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.name', read_only=True)
    region_code = serializers.CharField(source='region.code', read_only=True)
    parameter_name = serializers.CharField(source='parameter.name', read_only=True)
    parameter_code = serializers.CharField(source='parameter.code', read_only=True)
    parameter_unit = serializers.CharField(source='parameter.unit', read_only=True)
    
    class Meta:
        model = WeatherData
        fields = [
            'id', 'region', 'region_name', 'region_code',
            'parameter', 'parameter_name', 'parameter_code', 'parameter_unit',
            'year', 'month', 'value', 'created_at', 'updated_at'
        ]

class WeatherDataSummarySerializer(serializers.Serializer):
    region = serializers.CharField()
    parameter = serializers.CharField()
    year = serializers.IntegerField()
    avg_value = serializers.FloatField()
    min_value = serializers.FloatField()
    max_value = serializers.FloatField()
    count = serializers.IntegerField()

class DataSourceSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.name', read_only=True)
    parameter_name = serializers.CharField(source='parameter.name', read_only=True)
    
    class Meta:
        model = DataSource
        fields = '__all__'