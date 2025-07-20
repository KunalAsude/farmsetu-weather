from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class WeatherRegion(models.Model):
    """Model to store UK regions"""
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class WeatherParameter(models.Model):
    """Model to store weather parameters"""
    PARAMETER_CHOICES = [
        ('Tmax', 'Maximum Temperature'),
        ('Tmin', 'Minimum Temperature'),
        ('Tmean', 'Mean Temperature'),
        ('Sunshine', 'Sunshine Hours'),
        ('Rainfall', 'Rainfall'),
    ]
    
    code = models.CharField(max_length=20, choices=PARAMETER_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class WeatherData(models.Model):
    """Main model to store parsed weather data"""
    region = models.ForeignKey(WeatherRegion, on_delete=models.CASCADE)
    parameter = models.ForeignKey(WeatherParameter, on_delete=models.CASCADE)
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2030)])
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['region', 'parameter', 'year', 'month']
        ordering = ['-year', '-month']
    
    def __str__(self):
        return f"{self.region.code} - {self.parameter.code} - {self.year}/{self.month:02d}: {self.value}"

class DataSource(models.Model):
    """Model to track data sources and last update times"""
    url = models.URLField()
    region = models.ForeignKey(WeatherRegion, on_delete=models.CASCADE)
    parameter = models.ForeignKey(WeatherParameter, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['region', 'parameter']
    
    def __str__(self):
        return f"{self.region.code} - {self.parameter.code} Source"