# FarmSetu Weather Data API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A robust Django REST API for parsing, storing, and serving UK weather data from MetOffice's `UK.txt` format. This project provides clean, well-documented endpoints for accessing historical weather data with filtering and aggregation capabilities.

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [API Endpoints](#api-endpoints)
- [Local Development](#local-development)
- [Testing](#testing)
- [Docker Setup](#docker-setup)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

FarmSetu Weather Data API is a Django-based solution that:

- Parses raw weather data from MetOffice's `UK.txt` format
- Stores data in a structured SQLite database
- Exposes RESTful endpoints for data access
- Provides filtering and aggregation capabilities
- Includes a web dashboard for data visualization

## Project Structure

```
farmsetu_weather_project/
├── farmsetu_weather_project/    # Project configuration
│   ├── __init__.py
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py                 # WSGI config
├── weather/                    # Main app
│   ├── management/commands/    # Custom management commands
│   ├── migrations/             # Database migrations
│   ├── __init__.py
│   ├── admin.py               # Admin configuration
│   ├── apps.py                # App config
│   ├── models.py              # Database models
│   ├── parsers.py             # Data parsing logic
│   ├── serializers.py         # API serializers
│   ├── tests.py               # Test cases
│   ├── urls.py               # App URL configuration
│   └── views.py              # API views
├── static/                    # Static files (CSS, JS, images)
├── templates/                 # HTML templates
├── manage.py                  # Django management script
└── requirements.txt           # Project dependencies
```

## Key Features

- **Data Parsing**: Efficient parsing of MetOffice's `UK.txt` format
- **RESTful API**: Clean, well-documented endpoints following REST principles
- **Data Filtering**: Filter weather data by region, parameter, and date range
- **Data Aggregation**: Built-in support for data summarization
- **Admin Interface**: Built-in Django admin for data management
- **Test Coverage**: Comprehensive test suite for models and API endpoints

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/regions/` | GET | List all available regions |
| `/api/parameters/` | GET | List all weather parameters |
| `/api/weather-data/` | GET | List all weather data (filterable) |
| `/api/weather-data/<id>/` | GET | Get specific weather record |
| `/api/summary/` | GET | Get weather data summary |
| `/api/data-sources/` | GET | List available data sources |
| `/api/chart-data/` | GET | Get formatted data for charts |
| `/api/parse-data/` | POST | Trigger data parsing (admin only) |

### Query Parameters

Most list endpoints support filtering using query parameters:

- `region`: Filter by region code (e.g., `UK`)
- `parameter`: Filter by parameter code (e.g., `Tmean` for mean temperature)
- `year`: Filter by specific year
- `month`: Filter by specific month (1-12)

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd farmsetu-weather-api
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Load sample data (if available)**
   ```bash
   python manage.py loaddata weather/fixtures/initial_data.json
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - API Root: http://127.0.0.1:8000/api/
   - Admin Interface: http://127.0.0.1:8000/admin/

## Testing

Run the test suite:

```bash
python manage.py test weather
```

For coverage reporting (if coverage.py is installed):

```bash
coverage run --source='.' manage.py test weather
coverage report
```

## Docker Setup

1. **Build the Docker image**
   ```bash
   docker build -t farmsetu-weather-api .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 farmsetu-weather-api
   ```

## Deployment

For production deployment, consider the following components:

### Application Server
- Gunicorn or uWSGI

### Database
- PostgreSQL (recommended for production)
- MySQL
- SQLite (development only)

### Web Server
- Nginx (recommended)
- Apache

### Environment Variables

Set the following environment variables for production:

```bash
export DJANGO_SECRET_KEY='your-secret-key'
export DEBUG=False
export ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'
export DATABASE_URL='your-database-url'
```

### Example Gunicorn Command

```bash
gunicorn --workers 3 --bind 0.0.0.0:8000 farmsetu_weather_project.wsgi:application
```

### Code Style

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Maintain test coverage above 80%

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Note**: This is a sample weather data API project. Ensure you have proper authorization before using MetOffice data in production environments.
