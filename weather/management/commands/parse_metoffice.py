
from django.core.management.base import BaseCommand
from weather.parsers import MetOfficeParser

class Command(BaseCommand):
    help = 'Parse weather data from UK MetOffice'
    
    def add_arguments(self, parser):
        parser.add_argument('--region', type=str, help='Specific region to parse')
        parser.add_argument('--parameter', type=str, help='Specific parameter to parse')
    
    def handle(self, *args, **options):
        parser = MetOfficeParser()
        
        region = options.get('region')
        parameter = options.get('parameter')
        
        if region and parameter:
            self.stdout.write(f'Parsing data for {region} - {parameter}...')
            result = parser.parse_and_save(region, parameter)
            
            if result['success']:
                self.stdout.write(
                    self.style.SUCCESS(result['message'])
                )
            else:
                self.stdout.write(
                    self.style.ERROR(result['message'])
                )
        else:
            self.stdout.write('Parsing all weather data...')
            results = parser.parse_all_data()
            
            success_count = sum(1 for r in results if r['success'])
            total_count = len(results)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Completed parsing. {success_count}/{total_count} operations successful.'
                )
            )
            
            # Show failed operations
            for result in results:
                if not result['success']:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Failed: {result['region']} - {result['parameter']}: {result.get('error', 'Unknown error')}"
                        )
                    )