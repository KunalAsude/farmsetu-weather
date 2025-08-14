
from django.shortcuts import render
from .models import WeatherRecord, SeasonalWeatherRecord
from .serializers import WeatherRecordSerializer
from .parsers import DataParser
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView

class WeatherRecordViewSet(viewsets.ModelViewSet):
    queryset = WeatherRecord.objects.all()
    serializer_class = WeatherRecordSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['region', 'parameter', 'year', 'month']
    ordering_fields = ['region', 'parameter', 'year', 'month', 'value']

class ParseWeatherRecordView(APIView):
    def post(self, request):
        parser = DataParser()
        region = request.data.get('region')
        parameter = request.data.get('parameter')
        if region and parameter:
            parser.parse_and_save(region, parameter)
            return Response({'success': True, 'message': f'Data parsed for {region} {parameter}'})
        else:
            parser.parse_all_data()
            return Response({'success': True, 'message': 'All data parsed'})

def weather_list(request):
    region = request.GET.get('region')
    parameter = request.GET.get('parameter')
    year = request.GET.get('year')

    # Monthly data (direct queryset, new model structure)
    records_qs = WeatherRecord.objects.all()
    if region:
        records_qs = records_qs.filter(region=region)
    if year:
        records_qs = records_qs.filter(year=year)
    param_list = ['Tmax', 'Tmin', 'Tmean', 'Sunshine', 'Rainfall']
    records_qs = records_qs.order_by('region', '-year', 'month')
    records = records_qs
    total_count = records_qs.count()

    # Seasonal data
    seasonal_records = SeasonalWeatherRecord.objects.all()
    if region:
        seasonal_records = seasonal_records.filter(weather_record__region=region)
    if parameter:
        seasonal_records = seasonal_records.filter(weather_record__parameter=parameter)
    if year:
        seasonal_records = seasonal_records.filter(weather_record__year=year)
    total_seasonal = seasonal_records.count()
    seasonal_records = seasonal_records.order_by('-weather_record__year', 'season')

    seasons = SeasonalWeatherRecord.objects.values_list('season', flat=True).distinct()
    month_names = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    context = {
        'records': records,
        'param_list': param_list,
        'seasonal_records': seasonal_records,
        'regions': WeatherRecord.objects.values_list('region', flat=True).distinct(),
        'seasons': seasons,
        'total_count': total_count,
        'total_seasonal': total_seasonal,
        'month_names': month_names,
    }
    return render(request, 'weather/weather_list.html', context)

