from django.urls import path
from . import views

urlpatterns = [
    # Frontend URLs
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('charts/', views.charts, name='charts'),
    
    # API URLs
    path('api/regions/', views.WeatherRegionListView.as_view(), name='api-regions'),
    path('api/parameters/', views.WeatherParameterListView.as_view(), name='api-parameters'),
    path('api/weather-data/', views.WeatherDataListView.as_view(), name='api-weather-data'),
    path('api/weather-data/<int:pk>/', views.WeatherDataDetailView.as_view(), name='api-weather-detail'),
    path('api/parse-data/', views.ParseDataView.as_view(), name='api-parse-data'),
    path('api/summary/', views.WeatherSummaryView.as_view(), name='api-summary'),
    path('api/data-sources/', views.DataSourceListView.as_view(), name='api-data-sources'),
    path('api/chart-data/', views.chart_data, name='api-chart-data'),
]