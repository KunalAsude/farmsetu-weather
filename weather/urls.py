
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'weather'

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'weather-records', views.WeatherRecordViewSet, basename='weatherrecord')

urlpatterns = [
    # Frontend URL for weather list
    path('', views.weather_list, name='weather_list'),

    # API URLs
    path('api/weather-records/parse/', views.ParseWeatherRecordView.as_view(), name='api-parse-weather-records'),
    path('api/', include(router.urls)),
]