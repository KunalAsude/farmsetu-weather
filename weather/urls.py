from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'weather'  # This defines the application namespace

urlpatterns = [
    # Frontend URLs
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('charts/', views.charts, name='charts'),
    
    # API URLs
    path('api/', include([
        # API Documentation
        path('', get_schema_view(
            title="Weather API",
            description="API for accessing weather data",
            version="1.0.0"
        ), name='schema'),
        path('docs/', include_docs_urls(
            title='Weather API Documentation',
            description='Interactive API documentation for the Weather Data service'
        ), name='docs'),
        
        # API Endpoints
        path('regions/', views.WeatherRegionListView.as_view(), name='api-regions'),
        path('parameters/', views.WeatherParameterListView.as_view(), name='api-parameters'),
        path('weather-data/', views.WeatherDataListView.as_view(), name='api-weather-data'),
        path('weather-data/<int:pk>/', views.WeatherDataDetailView.as_view(), name='api-weather-detail'),
        path('parse-data/', views.ParseDataView.as_view(), name='api-parse-data'),
        path('summary/', views.WeatherSummaryView.as_view(), name='api-summary'),
        path('data-sources/', views.DataSourceListView.as_view(), name='api-data-sources'),
        path('chart-data/', views.chart_data, name='api-chart-data'),
    ])),
]