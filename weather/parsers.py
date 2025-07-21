import requests
import re
from datetime import datetime
from typing import List, Dict, Any
from .models import WeatherData, WeatherRegion, WeatherParameter, DataSource

class MetOfficeParser:
    """Parser for UK MetOffice weather data"""
    
    BASE_URL = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets"
    
    REGIONS = {
        'UK': 'United Kingdom',
        'England': 'England',
        'Wales': 'Wales',
        'Scotland': 'Scotland',
        'Northern_Ireland': 'Northern Ireland',
    }
    
    PARAMETERS = {
        'Tmax': {'name': 'Maximum Temperature', 'unit': '°C'},
        'Tmin': {'name': 'Minimum Temperature', 'unit': '°C'},
        'Tmean': {'name': 'Mean Temperature', 'unit': '°C'},
        'Sunshine': {'name': 'Sunshine Hours', 'unit': 'hours'},
        'Rainfall': {'name': 'Rainfall', 'unit': 'mm'},
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _parse_csv(self, csv_text):
        """
        Parse CSV text into a list of dictionaries.
        
        Args:
            csv_text (str): CSV formatted text data
            
        Returns:
            list: List of dictionaries containing the parsed data
            
        Raises:
            ValueError: If the CSV is malformed, empty, or doesn't contain required fields
        """
        import csv
        from io import StringIO
        
        if not csv_text or not csv_text.strip():
            raise ValueError("Empty CSV data provided")
            
        # Create a file-like object from the string
        csv_file = StringIO(csv_text.strip())
        
        try:
            # Try to parse the CSV data
            reader = csv.DictReader(csv_file)
            
            # Check if we have the required fields
            if not reader.fieldnames or 'year' not in reader.fieldnames or 'month' not in reader.fieldnames or 'value' not in reader.fieldnames:
                raise ValueError("CSV must contain 'year', 'month', and 'value' columns")
                
            # Convert to list of dictionaries
            result = []
            for row in reader:
                if not row:  # Skip empty rows
                    continue
                    
                # Validate required fields
                if not row.get('year') or not row.get('month') or not row.get('value'):
                    raise ValueError("Missing required fields in CSV row")
                    
                # Convert and validate field types
                try:
                    year = int(row['year'])
                    month = int(row['month'])
                    value = float(row['value'])
                    
                    result.append({
                        'year': year,
                        'month': month,
                        'value': value
                    })
                except (ValueError, TypeError) as e:
                    raise ValueError(f"Invalid data format in CSV: {str(e)}")
            
            if not result:
                raise ValueError("No valid data rows found in CSV")
                
            return result
            
        except csv.Error as e:
            raise ValueError(f"Error parsing CSV data: {str(e)}")
        except Exception as e:
            # Convert any other exception to ValueError for consistency
            raise ValueError(f"Error processing CSV: {str(e)}")
    
    def initialize_regions_and_parameters(self):
        """Initialize regions and parameters in database"""
        for code, name in self.REGIONS.items():
            WeatherRegion.objects.get_or_create(
                code=code,
                defaults={'name': name, 'description': f'Weather data for {name}'}
            )
        
        for code, info in self.PARAMETERS.items():
            WeatherParameter.objects.get_or_create(
                code=code,
                defaults={
                    'name': info['name'],
                    'unit': info['unit'],
                    'description': f'{info["name"]} measurements in {info["unit"]}'
                }
            )
    
    def get_data_url(self, region: str, parameter: str) -> str:
        """Generate URL for specific region and parameter"""
        return f"{self.BASE_URL}/{parameter}/date/{region}.txt"
    
    def fetch_data(self, url: str) -> str:
        """Fetch data from URL"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch data from {url}: {str(e)}")
    
    def parse_data_content(self, content: str) -> List[Dict[str, Any]]:
        """Parse the content of weather data file"""
        print(f"Debug: Starting to parse content. Content length: {len(content)} characters")
        print("Debug: First 200 chars of content:", content[:200])
        
        lines = content.strip().split('\n')
        print(f"Debug: Found {len(lines)} lines in content")
        
        data_lines = []
        
        # Skip header lines and find data start
        data_started = False
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('Provisional'):
                print(f"Debug: Skipping line {i+1}: {line[:50]}...")
                continue
            
            # Look for year pattern (4 digits)
            if re.match(r'^\d{4}', line):
                data_started = True
                print(f"Debug: Found data start at line {i+1}: {line[:50]}...")
            
            if data_started:
                data_lines.append(line)
        
        print(f"Debug: Found {len(data_lines)} data lines after filtering")
        
        parsed_data = []
        
        for line_num, line in enumerate(data_lines, 1):
            parts = line.split()
            if len(parts) < 13:  # Year + 12 months
                print(f"Debug: Line {line_num} has too few parts: {line}")
                continue
            
            try:
                year = int(parts[0])
                monthly_values = parts[1:13]  # 12 monthly values
                print(f"Debug: Processing year {year} with values: {' '.join(monthly_values)}")
                
                for month, value_str in enumerate(monthly_values, 1):
                    # Handle missing values
                    if value_str in ['---', 'na', 'NA', '']:
                        print(f"Debug: Skipping missing value for year {year}, month {month}")
                        continue
                    
                    try:
                        value = float(value_str)
                        parsed_data.append({
                            'year': year,
                            'month': month,
                            'value': value
                        })
                    except ValueError:
                        continue
                        
            except (ValueError, IndexError):
                continue
        
        return parsed_data
    
    def save_weather_data(self, region_code: str, parameter_code: str, parsed_data: List[Dict[str, Any]]) -> int:
        """Save parsed data to database"""
        print(f"Debug: Starting to save {len(parsed_data)} records for {region_code} {parameter_code}")
        
        try:
            region = WeatherRegion.objects.get(code=region_code)
            parameter = WeatherParameter.objects.get(code=parameter_code)
            print(f"Debug: Found region {region.id} and parameter {parameter.id}")
        except WeatherRegion.DoesNotExist:
            error_msg = f"Region not found: {region_code}"
            print(f"Error: {error_msg}")
            raise Exception(error_msg)
        except WeatherParameter.DoesNotExist:
            error_msg = f"Parameter not found: {parameter_code}"
            print(f"Error: {error_msg}")
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"Error: {error_msg}")
            raise Exception(error_msg)
        
        saved_count = 0
        error_count = 0
        
        for i, data_point in enumerate(parsed_data, 1):
            try:
                weather_data, created = WeatherData.objects.update_or_create(
                    region=region,
                    parameter=parameter,
                    year=data_point['year'],
                    month=data_point['month'],
                    defaults={'value': data_point['value']}
                )
                if created:
                    saved_count += 1
                if i % 100 == 0 or i == len(parsed_data):
                    print(f"Debug: Processed {i}/{len(parsed_data)} records, saved {saved_count} new records")
            except Exception as e:
                error_count += 1
                print(f"Error saving record {i}: {str(e)}")
                print(f"Record data: {data_point}")
                if error_count >= 5:  # Stop after 5 errors to avoid flooding logs
                    print("Too many errors, stopping...")
                    break
        
        # Update data source
        try:
            url = self.get_data_url(region_code, parameter_code)
            print(f"Debug: Updating data source for {region_code} {parameter_code}")
            DataSource.objects.update_or_create(
                region=region,
                parameter=parameter,
                defaults={
                    'url': url,
                    'last_updated': datetime.now(),
                    'is_active': True
                }
            )
            print("Debug: Data source updated successfully")
        except Exception as e:
            print(f"Error updating data source: {str(e)}")
        
        print(f"Debug: Successfully saved {saved_count} out of {len(parsed_data)} records for {region_code} {parameter_code}")
        return saved_count
    
    def parse_and_save(self, region_code: str, parameter_code: str) -> Dict[str, Any]:
        """Complete parsing and saving process"""
        url = self.get_data_url(region_code, parameter_code)
        
        try:
            # Fetch data
            content = self.fetch_data(url)
            
            # Parse data
            parsed_data = self.parse_data_content(content)
            
            # Save to database
            saved_count = self.save_weather_data(region_code, parameter_code, parsed_data)
            
            return {
                'success': True,
                'region': region_code,
                'parameter': parameter_code,
                'url': url,
                'total_records': len(parsed_data),
                'saved_records': saved_count,
                'message': f'Successfully parsed and saved {saved_count} records for {region_code} {parameter_code}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'region': region_code,
                'parameter': parameter_code,
                'url': url,
                'error': str(e),
                'message': f'Failed to parse data for {region_code} {parameter_code}: {str(e)}'
            }
    
    def parse_all_data(self) -> List[Dict[str, Any]]:
        """Parse data for all regions and parameters"""
        self.initialize_regions_and_parameters()
        results = []
        
        for region_code in self.REGIONS.keys():
            for parameter_code in self.PARAMETERS.keys():
                result = self.parse_and_save(region_code, parameter_code)
                results.append(result)
        
        return results