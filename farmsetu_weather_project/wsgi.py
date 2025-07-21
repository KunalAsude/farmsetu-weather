"""
WSGI config for farmsetu_weather_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Add the project directory to the Python path
import sys
from pathlib import Path

# Calculate the project directory
project_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_dir))

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmsetu_weather_project.settings')

application = get_wsgi_application()
