
from django.db import models

class WeatherRecord(models.Model):
    @property
    def month_name(self):
        month_names = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        if self.month and 1 <= self.month <= 12:
            return month_names[self.month]
        return "-"
    region = models.CharField(max_length=32)
    year = models.IntegerField()
    month = models.IntegerField(null=True, blank=True)
    Tmax = models.FloatField(null=True, blank=True)
    Tmin = models.FloatField(null=True, blank=True)
    Tmean = models.FloatField(null=True, blank=True)
    Sunshine = models.FloatField(null=True, blank=True)
    Rainfall = models.FloatField(null=True, blank=True)

    def __str__(self):
        month_names = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        if self.month:
            month_str = month_names[self.month] if 1 <= self.month <= 12 else str(self.month)
            return f"{self.region} {self.year}-{month_str}: Tmax={self.Tmax}, Tmin={self.Tmin}, Tmean={self.Tmean}, Sunshine={self.Sunshine}, Rainfall={self.Rainfall}"
        else:
            return f"{self.region} {self.year}: Tmax={self.Tmax}, Tmin={self.Tmin}, Tmean={self.Tmean}, Sunshine={self.Sunshine}, Rainfall={self.Rainfall}"

class SeasonalWeatherRecord(models.Model):
    weather_record = models.ForeignKey(WeatherRecord, on_delete=models.CASCADE, related_name='seasonal_records')
    season = models.CharField(max_length=8)
    value = models.FloatField()

    def __str__(self):
        return f"{self.weather_record.region} {self.weather_record.parameter} {self.weather_record.year}-{self.season}: {self.value}"