from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import WeatherRegion, WeatherParameter, WeatherData
from .parsers import MetOfficeParser
import json

class WeatherModelTests(TestCase):
    """Test weather models"""
    
    def setUp(self):
        self.region = WeatherRegion.objects.create(
            code='UK',
            name='United Kingdom',
            description='UK weather data'
        )
        self.parameter = WeatherParameter.objects.create(
            code='Tmean',
            name='Mean Temperature',
            unit='°C'
        )
    
    def test_weather_region_creation(self):
        self.assertEqual(self.region.code, 'UK')
        self.assertEqual(str(self.region), 'United Kingdom (UK)')
    
    def test_weather_parameter_creation(self):
        self.assertEqual(self.parameter.code, 'Tmean')
        self.assertEqual(str(self.parameter), 'Mean Temperature (Tmean)')
    
    def test_weather_data_creation(self):
        weather_data = WeatherData.objects.create(
            region=self.region,
            parameter=self.parameter,
            year=2023,
            month=1,
            value=5.2
        )
        self.assertEqual(weather_data.value, 5.2)
        self.assertEqual(str(weather_data), 'UK - Tmean - 2023/01: 5.2')

class WeatherAPITests(APITestCase):
    """Test API endpoints"""
    
    def setUp(self):
        self.region = WeatherRegion.objects.create(
            code='UK',
            name='United Kingdom'
        )
        self.parameter = WeatherParameter.objects.create(
            code='Tmean',
            name='Mean Temperature',
            unit='°C'
        )
        self.weather_data = WeatherData.objects.create(
            region=self.region,
            parameter=self.parameter,
            year=2023,
            month=1,
            value=5.2
        )
    
    def test_regions_api(self):
        url = reverse('weather:api-regions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if response is paginated (has 'results' key)
        if 'results' in response.data:
            regions = response.data['results']
        else:
            regions = response.data
            
        # Check that we get at least 1 region (the one we created in setUp)
        self.assertGreaterEqual(len(regions), 1)
        # Verify our test region is in the response
        region_codes = [r['code'] for r in regions]
        self.assertIn('UK', region_codes)
    
    def test_parameters_api(self):
        url = reverse('weather:api-parameters')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if response is paginated (has 'results' key)
        if 'results' in response.data:
            parameters = response.data['results']
        else:
            parameters = response.data
            
        # Check that we get at least 1 parameter (the one we created in setUp)
        self.assertGreaterEqual(len(parameters), 1)
        # Verify our test parameter is in the response
        parameter_codes = [p['code'] for p in parameters]
        self.assertIn('Tmean', parameter_codes)
    
    def test_weather_data_api(self):
        url = reverse('weather:api-weather-data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_weather_data_filtering(self):
        url = reverse('weather:api-weather-data')
        response = self.client.get(url, {'region': 'UK', 'parameter': 'Tmean'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_summary_api(self):
        url = reverse('weather:api-summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify response structure
        self.assertIn('total_records', response.data)
        self.assertIn('data_range', response.data)
        self.assertIn('regions', response.data)
        self.assertIn('parameters', response.data)
        self.assertIn('summary', response.data)
        # Verify data types
        self.assertIsInstance(response.data['total_records'], int)
        self.assertIsInstance(response.data['data_range'], dict)
        self.assertIsInstance(response.data['regions'], list)
        self.assertIsInstance(response.data['parameters'], list)
        self.assertIsInstance(response.data['summary'], list)
    
    def test_chart_data_api(self):
        url = reverse('weather:api-chart-data')
        response = self.client.get(url, {'parameter': 'Tmean'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify response structure matches the actual API
        self.assertIn('labels', response.data)
        self.assertIn('values', response.data)
        self.assertIn('region', response.data)
        self.assertIn('parameter', response.data)
        # Verify data types
        self.assertIsInstance(response.data['labels'], list)
        self.assertIsInstance(response.data['values'], list)
        self.assertIsInstance(response.data['region'], str)
        self.assertIsInstance(response.data['parameter'], str)
    
    def test_parse_data_api_unauthorized(self):
        url = reverse('weather:api-parse-data')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class MetOfficeParserTests(TestCase):
    """Test MetOfficeParser functionality"""
    
    def test_parse_csv_data(self):
        # Test with sample CSV data
        csv_data = """
        year,month,value
        2023,1,5.2
        2023,2,6.1
        """
        parser = MetOfficeParser()
        result = parser._parse_csv(csv_data)
        self.assertEqual(len(result), 2)
        # The actual implementation returns a list of dictionaries with string values
        self.assertEqual(int(result[0]['year']), 2023)
        self.assertEqual(int(result[0]['month']), 1)
        self.assertEqual(float(result[0]['value']), 5.2)

    def test_parse_invalid_csv(self):
        # Test with invalid CSV data
        csv_data = "invalid,csv,data"
        parser = MetOfficeParser()
        with self.assertRaises(ValueError):
            parser._parse_csv(csv_data)
    
    def test_parse_empty_csv(self):
        # Test with empty CSV data
        csv_data = ""
        parser = MetOfficeParser()
        with self.assertRaises(ValueError):
            parser._parse_csv(csv_data)