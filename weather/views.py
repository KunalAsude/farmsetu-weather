from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Avg, Min, Max, Count, Q
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import WeatherData, WeatherRegion, WeatherParameter, DataSource
from .serializers import (
    WeatherDataSerializer, WeatherRegionSerializer, 
    WeatherParameterSerializer, WeatherDataSummarySerializer,
    DataSourceSerializer
)
from .parsers import MetOfficeParser

# API Views
class WeatherRegionListView(generics.ListAPIView):
    """List all weather regions"""
    queryset = WeatherRegion.objects.all().order_by('name')
    serializer_class = WeatherRegionSerializer
    permission_classes = []  # No authentication required

class WeatherParameterListView(generics.ListAPIView):
    """List all weather parameters"""
    queryset = WeatherParameter.objects.all().order_by('code')
    serializer_class = WeatherParameterSerializer
    permission_classes = []  # No authentication required

class WeatherDataListView(generics.ListAPIView):
    """List weather data with filtering"""
    serializer_class = WeatherDataSerializer
    permission_classes = []  # No authentication required
    
    def get_queryset(self):
        queryset = WeatherData.objects.select_related('region', 'parameter')
        
        # Filter by region
        region = self.request.query_params.get('region', None)
        if region:
            queryset = queryset.filter(region__code=region)
        
        # Filter by parameter
        parameter = self.request.query_params.get('parameter', None)
        if parameter:
            queryset = queryset.filter(parameter__code=parameter)
        
        # Filter by year
        year = self.request.query_params.get('year', None)
        if year:
            queryset = queryset.filter(year=year)
        
        # Filter by year range
        year_from = self.request.query_params.get('year_from', None)
        year_to = self.request.query_params.get('year_to', None)
        if year_from:
            queryset = queryset.filter(year__gte=year_from)
        if year_to:
            queryset = queryset.filter(year__lte=year_to)
        
        return queryset.order_by('-year', '-month')

class WeatherDataDetailView(generics.RetrieveAPIView):
    """Get specific weather data record"""
    queryset = WeatherData.objects.select_related('region', 'parameter')
    serializer_class = WeatherDataSerializer
    permission_classes = []  # No authentication required

@method_decorator(csrf_exempt, name='dispatch')
class ParseDataView(APIView):
    """
    API to trigger data parsing
    Requires authentication to prevent unauthorized data parsing
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        parser = MetOfficeParser()
        
        region = request.data.get('region', None)
        parameter = request.data.get('parameter', None)
        
        if region and parameter:
            # Parse specific region and parameter
            result = parser.parse_and_save(region, parameter)
            return Response(result)
        else:
            # Parse all data
            results = parser.parse_all_data()
            return Response({
                'success': True,
                'message': 'Data parsing completed',
                'results': results
            })

class WeatherSummaryView(APIView):
    """Get weather data summary with statistics"""
    
    def get(self, request):
        region = request.query_params.get('region', None)
        parameter = request.query_params.get('parameter', None)
        year = request.query_params.get('year', None)
        
        queryset = WeatherData.objects.all()
        
        if region:
            queryset = queryset.filter(region__code=region)
        if parameter:
            queryset = queryset.filter(parameter__code=parameter)
        if year:
            queryset = queryset.filter(year=year)
        
        # Get total record count
        total_records = queryset.count()
        
        # Get date range
        date_range = queryset.aggregate(
            min_year=Min('year'),
            max_year=Max('year')
        )
        
        # Get unique regions and parameters
        regions = list(WeatherRegion.objects.values('code', 'name').distinct())
        parameters = list(WeatherParameter.objects.values('code', 'name').distinct())
        
        # Group by region, parameter, and year for detailed statistics
        summary = queryset.values(
            'region__name', 'parameter__name', 'year'
        ).annotate(
            avg_value=Avg('value'),
            min_value=Min('value'),
            max_value=Max('value'),
            count=Count('value')
        ).order_by('-year')
        
        # Prepare the response data
        response_data = {
            'total_records': total_records,
            'data_range': {
                'min_year': date_range['min_year'],
                'max_year': date_range['max_year']
            },
            'regions': regions,
            'parameters': parameters,
            'summary': list(summary)
        }
        
        return Response(response_data)

class DataSourceListView(generics.ListAPIView):
    """List all data sources"""
    queryset = DataSource.objects.select_related('region', 'parameter').order_by('region__name', 'parameter__name')
    serializer_class = DataSourceSerializer

# Frontend Views
def dashboard(request):
    """Main dashboard view"""
    regions = WeatherRegion.objects.all()
    parameters = WeatherParameter.objects.all()
    
    # Get some basic statistics
    total_records = WeatherData.objects.count()
    latest_year = WeatherData.objects.aggregate(Max('year'))['year__max']
    earliest_year = WeatherData.objects.aggregate(Min('year'))['year__min']
    
    context = {
        'regions': regions,
        'parameters': parameters,
        'total_records': total_records,
        'latest_year': latest_year,
        'earliest_year': earliest_year,
    }
    
    return render(request, 'weather/dashboard.html', context)

def charts(request):
    """Charts and visualization view"""
    return render(request, 'weather/charts.html')

@api_view(['GET'])
def chart_data(request):
    """API endpoint for chart data"""
    region = request.GET.get('region', 'UK')
    parameter = request.GET.get('parameter', 'Tmean')
    
    data = WeatherData.objects.filter(
        region__code=region,
        parameter__code=parameter
    ).order_by('year', 'month').values('year', 'month', 'value')
    
    # Format data for charts
    chart_data = {
        'labels': [],
        'values': [],
        'region': region,
        'parameter': parameter
    }
    
    for record in data:
        chart_data['labels'].append(f"{record['year']}-{record['month']:02d}")
        chart_data['values'].append(record['value'])
    
    return Response(chart_data)