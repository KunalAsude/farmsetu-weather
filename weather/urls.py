from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from . import views

# API Patterns
api_patterns = [
    path('regions/', views.WeatherRegionListView.as_view(), name='api-regions'),
    path('parameters/', views.WeatherParameterListView.as_view(), name='api-parameters'),
    path('weather-data/', views.WeatherDataListView.as_view(), name='api-weather-data'),
    path('weather-data/<int:pk>/', views.WeatherDataDetailView.as_view(), name='api-weather-detail'),
    path('parse-data/', views.ParseDataView.as_view(), name='api-parse-data'),
    path('summary/', views.WeatherSummaryView.as_view(), name='api-summary'),
    path('data-sources/', views.DataSourceListView.as_view(), name='api-data-sources'),
    path('chart-data/', views.chart_data, name='api-chart-data'),
]

urlpatterns = [
    # Frontend URLs
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('charts/', views.charts, name='charts'),
    
    # API Documentation
    path('api/', include([
        path('', get_schema_view(
            title="Weather API",
            description="API for accessing weather data",
            version="1.0.0"
        ), name='api-schema'),
        path('docs/', include_docs_urls(
            title='Weather API Documentation',
            description='Interactive API documentation for the Weather Data service'
        ), name='api-docs'),
        path('', include(api_patterns)),
    ])),
]