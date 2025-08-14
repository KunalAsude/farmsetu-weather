import requests
import re
from .models import WeatherRecord, SeasonalWeatherRecord

class DataParser:
    BASE_URL = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets"
    REGIONS = ['UK', 'England', 'Wales', 'Scotland', 'Northern_Ireland']
    PARAMETERS = ['Tmax', 'Tmin', 'Tmean', 'Sunshine', 'Rainfall']

    def get_data_url(self, region, parameter):
        return f"{self.BASE_URL}/{parameter}/date/{region}.txt"

    def fetch_data(self, url):
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    def parse_data_content(self, content):
        lines = content.strip().split('\n')
        data_lines = [line.strip() for line in lines if line.strip() and not line.startswith('#') and not line.startswith('Provisional') and re.match(r'^\d{4}', line)]
        monthly = []
        seasonal = []
        for line in data_lines:
            parts = line.split()
            if len(parts) < 13:
                continue
            year = int(parts[0])
            # Monthly
            for month, value_str in enumerate(parts[1:13], 1):
                if value_str not in ['---', 'na', 'NA', '']:
                    try:
                        value = float(value_str)
                        monthly.append({'year': year, 'month': month, 'value': value})
                    except Exception:
                        continue
            # Seasonal/annual
            period_names = ['win', 'spr', 'sum', 'aut', 'ann']
            for i, pname in enumerate(period_names, start=13):
                if len(parts) > i:
                    value_str = parts[i]
                    if value_str not in ['---', 'na', 'NA', '']:
                        try:
                            value = float(value_str)
                            seasonal.append({'year': year, 'season': pname, 'value': value})
                        except Exception:
                            continue
        return monthly, seasonal

    def save_weather_data(self, region, all_monthly, all_seasonal):
        # all_monthly: { (year, month): {param: value, ...} }
        for (year, month), param_dict in all_monthly.items():
            WeatherRecord.objects.update_or_create(
                region=region,
                year=year,
                month=month,
                defaults={
                    'Tmax': param_dict.get('Tmax'),
                    'Tmin': param_dict.get('Tmin'),
                    'Tmean': param_dict.get('Tmean'),
                    'Sunshine': param_dict.get('Sunshine'),
                    'Rainfall': param_dict.get('Rainfall'),
                }
            )
        # Save seasonal data: all_seasonal: { (year, season): {param: value, ...} }
        for (year, season), param_dict in all_seasonal.items():
            # Link to the January record for that year (or create if missing)
            weather_record, _ = WeatherRecord.objects.get_or_create(
                region=region,
                year=year,
                month=1
            )
            for param, value in param_dict.items():
                SeasonalWeatherRecord.objects.update_or_create(
                    weather_record=weather_record,
                    season=season,
                    defaults={'value': value}
                )


    def parse_and_save(self, region):
        # Collect all parameters for each (year, month) and (year, season)
        all_monthly = {}
        all_seasonal = {}
        for parameter in self.PARAMETERS:
            url = self.get_data_url(region, parameter)
            content = self.fetch_data(url)
            monthly, seasonal = self.parse_data_content(content)
            for entry in monthly:
                key = (entry['year'], entry['month'])
                if key not in all_monthly:
                    all_monthly[key] = {}
                all_monthly[key][parameter] = entry['value']
            for entry in seasonal:
                key = (entry['year'], entry['season'])
                if key not in all_seasonal:
                    all_seasonal[key] = {}
                all_seasonal[key][parameter] = entry['value']
        self.save_weather_data(region, all_monthly, all_seasonal)

    def parse_all_data(self):
        for region in self.REGIONS:
            self.parse_and_save(region)